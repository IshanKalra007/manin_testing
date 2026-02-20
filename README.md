# Manim Testing – Vynotes Backend

Manim animation environment with plugins for the [Vynotes](https://github.com/IshanKalra007/remix-of-remix-of-storymaker-studio) frontend. Converts study notes into math and educational animations.

## Contents

- **renderer/** – FastAPI backend that receives Manim code, renders to video, uploads to S3
- **VYNOTES_AI_PLUGIN_GUIDE.md** – Plugin selection guide for the Vynotes AI layer
- **plugins-reference.json** – Structured plugin metadata for programmatic use

## Installed Manim Plugins

| Plugin | Use Case |
|--------|----------|
| manim-Astronomy | Orbits, planets, stars, spacetime |
| manim-CAD_Drawing_Utils | Technical drawings, dimensions |
| manim-eng | Circuit diagrams |
| ManimML | Neural network visualizations |
| manim-physics | Waves, optics, mechanics |
| manim-stock-visualization | Stock price charts |
| manim-timeline | Timeline presentations |
| manim-meshes | 2D/3D meshes |
| manim-voiceover-plus | Voiceover narration |

## Quick Start

```bash
# Create venv and install
python -m venv venv
venv\Scripts\activate
pip install manim

# Run renderer locally
cd renderer
pip install -r requirements.txt
uvicorn app:app --reload
```

## Renderer API

**POST /render**

```json
{
  "code": "<Manim Python code>",
  "scene_name": "MyScene",
  "quality": "qm",
  "renderer": "cairo"
}
```

Use `renderer: "opengl"` for 3D plugins (Astronomy, ManimML, manim-meshes).

## License

MIT
