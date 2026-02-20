# Vynotes Manim Renderer

Backend API that receives Manim Python code, renders animations, uploads to S3, and returns video URLs.

## API

- **POST /render** – Render Manim code
  - Body: `{ "code": "...", "scene_name": "MyScene", "quality": "ql" }`
  - Returns: `{ "success": true, "video_url": "https://...", "job_id": "..." }`

- **GET /health** – Health check

## Local Development (no S3)

```bash
cd renderer
pip install -r requirements.txt
uvicorn app:app --reload
```

Without `S3_BUCKET`, renders succeed but `video_url` is null. Use for testing Manim only.

## Local Docker (no S3)

```bash
docker build -t vynotes-renderer .
docker run -p 8000:8000 vynotes-renderer
```

## Production (AWS EC2 + S3)

See [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md).

## Test

```bash
python test_render.py
```
