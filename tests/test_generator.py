import os
import tempfile
import pytest
from PIL import Image
from src.generator import DiffusersGenerator
from src.models import GenerationRequest

@pytest.fixture
def temp_output_dir():
    d = tempfile.mkdtemp()
    yield d
    for f in os.listdir(d):
        os.remove(os.path.join(d, f))
    os.rmdir(d)

def test_generator_procedural_generation(temp_output_dir):
    gen = DiffusersGenerator()
    req = GenerationRequest(
        prompt="A mountain valley at dawn",
        width=256,
        height=256,
        steps=10,
        seed=100
    )
    res = gen.generate(req, output_dir=temp_output_dir)

    assert os.path.exists(res.output_path)
    assert res.seed == 100
    assert res.width == 256
    assert res.height == 256
    assert res.elapsed_seconds > 0

    # Verify PNG validity
    with Image.open(res.output_path) as img:
        assert img.size == (256, 256)
        assert img.format == "PNG"

def test_generator_seed_reproducibility(temp_output_dir):
    gen = DiffusersGenerator()
    req1 = GenerationRequest(prompt="Neon city", width=128, height=128, steps=5, seed=42)
    req2 = GenerationRequest(prompt="Neon city", width=128, height=128, steps=5, seed=42)

    res1 = gen.generate(req1, output_dir=temp_output_dir)
    res2 = gen.generate(req2, output_dir=temp_output_dir)

    with open(res1.output_path, "rb") as f1, open(res2.output_path, "rb") as f2:
        # Images generated from same seed and prompt should produce identical files
        assert f1.read() == f2.read()
