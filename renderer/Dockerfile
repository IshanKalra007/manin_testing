FROM manimcommunity/manim:stable

USER root

# System deps for OpenGL headless rendering (3D scenes) and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    libegl1-mesa \
    libgles2-mesa \
    mesa-utils \
    fonts-noto \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*

# Python API dependencies
RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    boto3

# Manim plugins — each in its own layer for faster rebuilds
RUN pip install --no-cache-dir manim-physics manim-eng
RUN pip install --no-cache-dir manim-CAD_Drawing_Utils manim-ml
RUN pip install --no-cache-dir manim-stock-visualization manim-timeline
RUN pip install --no-cache-dir manim-lamination-builder manim-meshes
RUN pip install --no-cache-dir manim-voiceover-plus || true

WORKDIR /app
COPY app.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
