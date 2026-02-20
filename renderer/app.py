"""
Manim Renderer API for Vynotes
Receives Manim code, renders to video, uploads to S3, returns URL.
"""

import os
import subprocess
import tempfile
import uuid
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Vynotes Manim Renderer",
    description="Renders Manim animations from code and returns video URLs",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RenderRequest(BaseModel):
    """Request body for rendering."""

    code: str = Field(..., description="Full Manim Python code (must define a Scene class)")
    scene_name: str = Field(..., description="Name of the Scene class to render")
    quality: str = Field(default="ql", description="Manim quality: ql, qm, qh, qk")
    renderer: str = Field(
        default="cairo",
        description="Manim renderer: 'cairo' (2D) or 'opengl' (3D, required for manim-Astronomy)",
    )


class RenderResponse(BaseModel):
    """Response with video URL."""

    success: bool = True
    video_url: str | None = None
    error: str | None = None
    job_id: str | None = None


def _get_manim_quality_flag(quality: str) -> str:
    """Map quality string to Manim flag."""
    mapping = {"ql": "-ql", "qm": "-qm", "qh": "-qh", "qk": "-qk"}
    return mapping.get(quality.lower(), "-ql")


def _run_manim(
    code: str,
    scene_name: str,
    quality: str,
    output_dir: Path,
    renderer: str = "cairo",
) -> Path | None:
    """
    Write code to temp file, run Manim, return path to output video.
    """
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
        ]
        if renderer and renderer.lower() == "opengl":
            cmd.extend(["--renderer", "opengl"])
        result = subprocess.run(
            cmd,
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=600,  # 10 min max per render
        )

        if result.returncode != 0:
            raise RuntimeError(f"Manim failed:\n{result.stderr}\n{result.stdout}")

        # Find output: media/videos/<script_name>/<quality>/<scene_name>.mp4
        script_name = script_path.stem
        media_dir = output_dir / "media" / "videos" / script_name
        if not media_dir.exists():
            raise RuntimeError(f"Manim did not produce output in {media_dir}")

        # Get the quality folder (e.g. 480p15, 1080p60)
        quality_dirs = list(media_dir.iterdir())
        if not quality_dirs:
            raise RuntimeError("No quality output folder found")

        video_dir = quality_dirs[0]
        video_path = video_dir / f"{scene_name}.mp4"
        if not video_path.exists():
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

    s3 = boto3.client("s3")
    try:
        s3.upload_file(str(local_path), bucket, s3_key)
    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}")

    region = os.environ.get("AWS_REGION", "us-east-1")
    return f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"


@app.post("/render", response_model=RenderResponse)
def render(request: RenderRequest):
    """
    Render Manim code and return S3 video URL.
    """
    job_id = str(uuid.uuid4())[:8]

    # Basic validation: must contain Scene and the scene class
    if "Scene" not in request.code:
        raise HTTPException(400, "Code must define a Scene class")
    if request.scene_name not in request.code:
        raise HTTPException(400, f"Scene class '{request.scene_name}' not found in code")

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
            raise HTTPException(504, "Render timed out (max 10 minutes)")
        except RuntimeError as e:
            raise HTTPException(500, str(e))

        # Upload to S3 if configured
        s3_bucket = os.environ.get("S3_BUCKET")
        if s3_bucket:
            s3_key = f"vynotes/{job_id}/{request.scene_name}.mp4"
            try:
                video_url = _upload_to_s3(video_path, s3_key)
            except RuntimeError as e:
                raise HTTPException(500, str(e))
        else:
            # No S3: return info that video was rendered locally (dev mode)
            video_url = None

    return RenderResponse(
        success=True,
        video_url=video_url,
        job_id=job_id,
    )


@app.get("/health")
def health():
    """Health check for load balancer."""
    return {"status": "ok", "service": "manim-renderer"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
