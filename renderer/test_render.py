"""
Quick test script for the renderer API.
Run the renderer locally first: uvicorn app:app --reload
"""

import requests

RENDERER_URL = "http://localhost:8000"  # or your EC2 URL

SIMPLE_SCENE = '''
from manim import *

class TestScene(Scene):
    def construct(self):
        text = Text("Hello from Vynotes!", font_size=48)
        self.play(Write(text))
        self.wait(1)
'''

def test_health():
    r = requests.get(f"{RENDERER_URL}/health")
    print("Health:", r.json())
    assert r.status_code == 200

def test_render():
    r = requests.post(
        f"{RENDERER_URL}/render",
        json={
            "code": SIMPLE_SCENE,
            "scene_name": "TestScene",
            "quality": "ql",
        },
        timeout=120,
    )
    print("Status:", r.status_code)
    print("Response:", r.json())
    if r.status_code == 200 and r.json().get("video_url"):
        print("Video URL:", r.json()["video_url"])

if __name__ == "__main__":
    test_health()
    print("\nRendering test scene (may take 1-2 min)...")
    test_render()
