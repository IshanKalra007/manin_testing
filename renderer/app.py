"""
Manim Renderer API for Vynotes
Receives Manim code, renders to video, uploads to S3, returns URL.
"""

import logging
import os
import re
import subprocess
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("vynotes-renderer")

app = FastAPI(
    title="Vynotes Manim Renderer",
    description="Renders Manim animations from code and returns video URLs",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BLOCKED_PATTERNS = [
    r"\bos\.system\b",
    r"\bsubprocess\b",
    r"\b__import__\b",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bopen\s*\(",
    r"\brequests\b",
    r"\burllib\b",
    r"\bsocket\b",
    r"\bshutil\b",
]


class RenderRequest(BaseModel):
    code: str = Field(..., description="Full Manim Python code (must define a Scene class)")
    scene_name: str = Field(..., description="Name of the Scene class to render")
    quality: str = Field(default="ql", description="Manim quality: ql, qm, qh, qk")
    renderer: str = Field(
        default="cairo",
        description="Manim renderer: 'cairo' (2D) or 'opengl' (3D plugins)",
    )


class RenderResponse(BaseModel):
    success: bool = True
    video_url: str | None = None
    error: str | None = None
    job_id: str | None = None


def _validate_code(code: str) -> None:
    """Reject code with dangerous operations."""
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, code):
            raise ValueError(f"Code contains blocked pattern: {pattern}")


def _get_manim_quality_flag(quality: str) -> str:
    mapping = {"ql": "-ql", "qm": "-qm", "qh": "-qh", "qk": "-qk"}
    return mapping.get(quality.lower(), "-ql")


def _run_manim(
    code: str,
    scene_name: str,
    quality: str,
    output_dir: Path,
    renderer: str = "cairo",
) -> Path:
    """Write code to temp file, run Manim, return path to output video."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
        dir=output_dir,
    ) as f:
        f.write(code)
        script_path = Path(f.name)

    try:
        quality_flag = _get_manim_quality_flag(quality)
        cmd = [
            "python",
            "-m",
            "manim",
            str(script_path),
            scene_name,
            quality_flag,
            "--disable_caching",
        ]
        if renderer and renderer.lower() == "opengl":
            cmd.extend(["--renderer", "opengl", "--write_to_movie"])

        log.info("Running: %s", " ".join(cmd))
        result = subprocess.run(
            cmd,
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode != 0:
            stderr_tail = result.stderr[-2000:] if result.stderr else ""
            stdout_tail = result.stdout[-1000:] if result.stdout else ""
            raise RuntimeError(
                f"Manim failed:\n{stderr_tail}\n{stdout_tail}"
            )

        script_name = script_path.stem
        media_dir = output_dir / "media" / "videos" / script_name
        if not media_dir.exists():
            all_mp4 = list(output_dir.rglob("*.mp4"))
            if all_mp4:
                return all_mp4[0]
            raise RuntimeError(f"Manim did not produce output in {media_dir}")

        quality_dirs = list(media_dir.iterdir())
        if not quality_dirs:
            raise RuntimeError("No quality output folder found")

        video_dir = quality_dirs[0]
        video_path = video_dir / f"{scene_name}.mp4"
        if not video_path.exists():
            mp4s = list(video_dir.glob("*.mp4"))
            if mp4s:
                return mp4s[0]
            raise RuntimeError(f"Video not found: {video_path}")

        return video_path
    finally:
        script_path.unlink(missing_ok=True)


def _upload_to_s3(local_path: Path, s3_key: str) -> str:
    """Upload file to S3 and return public URL."""
    import boto3
    from botocore.exceptions import ClientError

    bucket = os.environ.get("S3_BUCKET")
    if not bucket:
        raise RuntimeError("S3_BUCKET environment variable not set")

    region = os.environ.get("AWS_REGION", "us-east-1")
    s3 = boto3.client("s3", region_name=region)
    try:
        s3.upload_file(
            str(local_path),
            bucket,
            s3_key,
            ExtraArgs={"ContentType": "video/mp4"},
        )
    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}")

    return f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"


@app.post("/render", response_model=RenderResponse)
def render(request: RenderRequest):
    """Render Manim code and return S3 video URL."""
    job_id = str(uuid.uuid4())[:8]
    log.info("Job %s: rendering %s (renderer=%s, quality=%s)",
             job_id, request.scene_name, request.renderer, request.quality)

    if "Scene" not in request.code:
        raise HTTPException(400, "Code must define a Scene class")
    if request.scene_name not in request.code:
        raise HTTPException(400, f"Scene class '{request.scene_name}' not found in code")

    try:
        _validate_code(request.code)
    except ValueError as e:
        raise HTTPException(400, str(e))

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        try:
            video_path = _run_manim(
                request.code,
                request.scene_name,
                request.quality,
                output_dir,
                renderer=request.renderer,
            )
        except subprocess.TimeoutExpired:
            log.error("Job %s: timed out", job_id)
            raise HTTPException(504, "Render timed out (max 10 minutes)")
        except RuntimeError as e:
            log.error("Job %s: render failed — %s", job_id, e)
            raise HTTPException(500, str(e))

        s3_bucket = os.environ.get("S3_BUCKET")
        if s3_bucket:
            s3_key = f"vynotes/{job_id}/{request.scene_name}.mp4"
            try:
                video_url = _upload_to_s3(video_path, s3_key)
            except RuntimeError as e:
                log.error("Job %s: S3 upload failed — %s", job_id, e)
                raise HTTPException(500, str(e))
        else:
            video_url = None

    log.info("Job %s: complete — %s", job_id, video_url)
    return RenderResponse(success=True, video_url=video_url, job_id=job_id)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "manim-renderer", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
