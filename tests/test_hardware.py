import pytest
from src.hardware import HardwareProfiler

def test_hardware_profiler_cpu():
    hw = HardwareProfiler.profile(force_device="cpu")
    assert hw.device == "cpu"
    assert hw.recommended_precision == "fp32"
    assert hw.max_resolution <= 512
    assert hw.ram_gb > 0

def test_hardware_profiler_ram_detection():
    ram = HardwareProfiler.get_system_ram_gb()
    assert isinstance(ram, float)
    assert ram >= 1.0

def test_hardware_profiler_auto():
    hw = HardwareProfiler.profile()
    assert hw.device in ("cuda", "cpu", "mps")
    assert hw.recommended_steps >= 10
