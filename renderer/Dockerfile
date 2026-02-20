# Base: Official Manim image (includes ffmpeg, cairo, pango, etc.)
FROM manimcommunity/manim:stable

# Install Python API dependencies
RUN pip install --no-cache-dir \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    pydantic>=2.0.0 \
    boto3>=1.28.0

# Copy renderer app
WORKDIR /app
COPY app.py .

# Manim writes to ./media by default; we'll use /tmp for renders
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
