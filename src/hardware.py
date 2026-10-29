import os
import sys
import platform
from typing import Optional
from src.models import HardwareProfile

class HardwareProfiler:
    """Probes system compute resources and derives optimal diffusion pipeline configuration."""

    @classmethod
    def get_system_ram_gb(cls) -> float:
        """Estimate total system RAM in GB."""
        try:
            if sys.platform == "win32":
                import ctypes
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return round(stat.ullTotalPhys / (1024**3), 1)
            elif sys.platform == "linux":
                with open("/proc/meminfo") as f:
                    for line in f:
                        if "MemTotal" in line:
                            return round(int(line.split()[1]) / (1024**2), 1)
        except Exception:
            pass
        return 16.0  # Safe default assumption

    @classmethod
    def profile(cls, force_device: Optional[str] = None) -> HardwareProfile:
        """Analyze available hardware and recommend execution parameters."""
        ram_gb = cls.get_system_ram_gb()

        # Check PyTorch CUDA
        cuda_available = False
        vram_gb = 0.0
        device_name = "CPU"
        try:
            import torch
            if torch.cuda.is_available() and force_device != "cpu":
                cuda_available = True
                device_name = torch.cuda.get_device_name(0)
                vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 1)
        except ImportError:
            pass

        # Decide profile based on device
        if cuda_available and force_device != "cpu":
            device = "cuda"
            if vram_gb >= 12.0:
                precision = "fp16"
                max_res = 1024
                steps = 30
                slice_attn = False
                offload = False
            elif vram_gb >= 6.0:
                precision = "fp16"
                max_res = 768
                steps = 25
                slice_attn = True
                offload = False
            else:  # Under 6 GB VRAM
                precision = "fp16"
                max_res = 512
                steps = 20
                slice_attn = True
                offload = True
        else:
            device = "cpu"
            device_name = f"Multi-threaded CPU ({platform.processor() or 'x86_64'})"
            vram_gb = 0.0
            precision = "fp32"
            max_res = 512
            steps = 15
            slice_attn = True
            offload = False

        return HardwareProfile(
            device=device,
            device_name=device_name,
            vram_gb=vram_gb,
            ram_gb=ram_gb,
            recommended_precision=precision,
            max_resolution=max_res,
            recommended_steps=steps,
            attention_slicing=slice_attn,
            sequential_offload=offload,
        )
