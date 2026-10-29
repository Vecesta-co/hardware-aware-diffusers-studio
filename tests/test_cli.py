import subprocess
import sys
import os
import tempfile
import pytest

def test_cli_help():
    res = subprocess.run([sys.executable, "-m", "src.cli", "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "hardware-aware-diffusers-studio" in res.stdout
    assert "generate" in res.stdout
    assert "hardware" in res.stdout

def test_cli_hardware():
    res = subprocess.run([sys.executable, "-m", "src.cli", "hardware"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Hardware Profiling Results" in res.stdout
    assert "Recommended Precision" in res.stdout

def test_cli_optimize():
    res = subprocess.run([sys.executable, "-m", "src.cli", "optimize", "dragon on a mountain"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Enhanced Prompt" in res.stdout

def test_cli_generate():
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        out_png = f.name
    try:
        res = subprocess.run(
            [
                sys.executable, "-m", "src.cli", "generate",
                "A futuristic metropolis", "-o", out_png,
                "-w", "256", "-H", "256", "-s", "10", "--cpu"
            ],
            capture_output=True,
            text=True
        )
        assert res.returncode == 0
        assert "generated successfully" in res.stdout
        assert os.path.exists(out_png)
        assert os.path.getsize(out_png) > 1000
    finally:
        if os.path.exists(out_png):
            os.remove(out_png)
