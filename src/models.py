from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class HardwareProfile(BaseModel):
    """Hardware capability and tuned configuration."""
    device: str  # cuda, mps, cpu, directml
    device_name: str
    vram_gb: float
    ram_gb: float
    recommended_precision: str  # fp16, bf16, fp32
    max_resolution: int
    recommended_steps: int
    attention_slicing: bool
    sequential_offload: bool

class GenerationRequest(BaseModel):
    """Image generation parameter specification."""
    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 512
    height: int = 512
    steps: int = 25
    seed: Optional[int] = None
    guidance_scale: float = 7.5
    optimize_prompt: bool = True

class GenerationResult(BaseModel):
    """Output generation result and hardware telemetry."""
    output_path: str
    width: int
    height: int
    seed: int
    elapsed_seconds: float
    device_used: str
    precision_used: str
    optimized_prompt: str
