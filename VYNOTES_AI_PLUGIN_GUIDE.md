# Manim Plugin Guide for Vynotes AI

**Purpose:** Add this to your Vynotes AI system prompt so it knows which Manim plugins exist and when to use them when generating code from study notes.

---

## Plugin Decision Matrix

| Study notes mention... | Use plugin | Renderer | Key imports |
|------------------------|------------|----------|-------------|
| orbits, planets, stars, solar system, spacetime, black holes | manim-Astronomy | **opengl** | `from manim_Astronomy.stellar_objects import Planet, Star` |
| circuits, resistors, capacitors, voltage, electronics | manim-eng | cairo | `from manim_eng import *` |
| neural networks, CNN, machine learning, layers, neurons | ManimML | **opengl** | `from manim_ml.neural_network import NeuralNetwork, FeedForwardLayer, Convolutional2DLayer` |
| physics, waves, optics, mechanics, electromagnetism | manim-physics | cairo | `from manim_physics import *` |
| stock prices, portfolio, finance, market data | manim-stock-visualization | cairo | `from manim_stock.visualization import Lineplot, GrowingLineplot` |
| timeline, literature review, historical events | manim-timeline | cairo | manim-timeline classes |
| dimensions, CAD, technical drawing, rounded corners | manim-CAD_Drawing_Utils | cairo | `from manim_cad_drawing_utils import Round_Corners, Linear_Dimension` |
| meshes, triangulation, Delaunay, 3D meshes | manim-meshes | **opengl** | `from manim_meshes import *` |
| voiceover, narration, spoken explanation | manim-voiceover-plus | cairo | `from manim_voiceover_plus import VoiceoverScene` |
| lamination, Julia sets, complex dynamics | manim-lamination-builder | cairo | `from manim_lamination_builder import parse_lamination, Main` |

**Default:** Use `cairo` renderer. Use `opengl` only when the plugin requires 3D (Astronomy, ManimML 3D, manim-meshes).

---

## Renderer API Request

When calling the renderer, include the correct `renderer` field:

```json
{
  "code": "<generated Manim Python code>",
  "scene_name": "MyScene",
  "quality": "ql",
  "renderer": "opengl"
}
```

- `"cairo"` — 2D animations (default)
- `"opengl"` — 3D animations, manim-Astronomy, ManimML, manim-meshes

---

## Content → Plugin Triggers

**Astronomy:** orbit, planet, star, solar system, black hole, spacetime, gravity, Kepler, ellipse  
**Circuits:** circuit, resistor, capacitor, voltage, current, Ohm, Kirchhoff  
**ML/Neural:** neural network, CNN, layer, neuron, activation, dropout, convolution  
**Physics:** wave, optics, lens, mirror, electromagnetism, mechanics, collision  
**Finance:** stock, portfolio, price, market, chart, yfinance  
**Timeline:** timeline, literature, publication, history, chronology  
**CAD:** dimension, chamfer, rounded corner, technical drawing, blueprint  
**Meshes:** mesh, triangulation, Delaunay, Voronoi, 3D mesh  
**Voiceover:** voiceover, narration, spoken, audio, explain aloud  

---

## Quick Import Reference

```python
# Astronomy (opengl)
from manim_Astronomy.stellar_objects import Planet, Star
config.renderer = "opengl"

# Circuits
from manim_eng import *

# Neural networks (opengl)
from manim_ml.neural_network import NeuralNetwork, FeedForwardLayer, Convolutional2DLayer

# Physics
from manim_physics import *

# Stock charts
from manim_stock.visualization import Lineplot, GrowingLineplot
from manim_stock.util import download_stock_data, preprocess_stock_data

# CAD
from manim_cad_drawing_utils import Round_Corners, Chamfer_Corners, Linear_Dimension

# Meshes (opengl)
from manim_meshes import *
config.renderer = "opengl"
```
