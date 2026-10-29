import urllib.request
import json
import time
import os
import pytest
from src.studio import run_studio
from src.generator import DiffusersGenerator

@pytest.fixture(scope="module")
def studio_server():
    port = 7891
    gen = DiffusersGenerator()
    server = run_studio(generator=gen, host="127.0.0.1", port=port, background=True)
    time.sleep(0.5)
    url = f"http://127.0.0.1:{port}"
    yield url
    server.shutdown()

def test_studio_health(studio_server):
    with urllib.request.urlopen(f"{studio_server}/health") as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        assert data["status"] == "ok"

def test_studio_html(studio_server):
    with urllib.request.urlopen(f"{studio_server}/") as resp:
        assert resp.status == 200
        html = resp.read().decode()
        assert "Diffusers Studio" in html

def test_studio_api_hardware(studio_server):
    with urllib.request.urlopen(f"{studio_server}/api/hardware") as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        assert "device" in data
        assert "recommended_precision" in data

def test_studio_api_generate(studio_server):
    payload = json.dumps({
        "prompt": "An enchanted forest with bioluminescent mushrooms",
        "width": 256,
        "height": 256,
        "steps": 10
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{studio_server}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        assert "output_path" in data
        assert os.path.exists(data["output_path"])
        # Clean up output file
        if os.path.exists(data["output_path"]):
            os.remove(data["output_path"])
