import pytest
from src.models import HardwareProfile, GenerationRequest, GenerationResult

def test_hardware_profile_model():
    hw = HardwareProfile(
        device="cuda",
        device_name="NVIDIA RTX 4090",
        vram_gb=24.0,
        ram_gb=64.0,
        recommended_precision="fp16",
        max_resolution=1024,
        recommended_steps=30,
        attention_slicing=False,
        sequential_offload=False
    )
    assert hw.device == "cuda"
    assert hw.max_resolution == 1024
    assert hw.vram_gb == 24.0

def test_generation_request_model():
    req = GenerationRequest(
        prompt="A cosmic landscape",
        width=768,
        height=512,
        steps=25
    )
    assert req.width == 768
    assert req.steps == 25
    assert req.optimize_prompt is True

def test_generation_result_model():
    res = GenerationResult(
        output_path="test.png",
        width=512,
        height=512,
        seed=1234,
        elapsed_seconds=1.2,
        device_used="cpu",
        precision_used="fp32",
        optimized_prompt="A cosmic landscape, 8k"
    )
    assert res.seed == 1234
    assert res.elapsed_seconds == 1.2
