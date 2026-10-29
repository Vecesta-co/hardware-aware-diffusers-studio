# PLAN.md — hardware-aware-diffusers-studio

## 1. Executive Summary

`hardware-aware-diffusers-studio` is an open-source, hardware-aware image generation playground and headless inference studio developed by Vecesta.co. It dynamically inspects available accelerator hardware (NVIDIA CUDA VRAM, Apple Silicon MPS, DirectML, and multi-threaded CPU), tunes precision (FP16/BF16/FP32) and memory slicing to prevent out-of-memory (OOM) crashes, features automated prompt enhancement, and provides both a terminal CLI and a modern glassmorphism web studio.

---

## 2. Competitive Landscape & Reference Analysis

- **Reference**: `AUTOMATIC1111/stable-diffusion-webui` (AGPL 3.0).
- **Rules & Gaps**:
  - WebUI is strictly AGPL 3.0, precluding MIT distribution. Our studio is built cleanly from first principles under permissive MIT.
  - WebUI is a massive monolithic 15+ GB environment that frequently crashes with CUDA OOM on machines with <6 GB VRAM unless obscure CLI arguments (`--medvram`, `--opt-sub-quad-attention`) are manually discovered.
  - WebUI lacks automatic hardware adaptation and graceful, zero-install CPU fallback.
- **How We Are Different & More Capable**:
  1. **Dynamic Hardware Profiler**: Automatically probes GPU VRAM, compute capability, and RAM to determine optimal precision (fp16, fp32), attention slicing, and max resolution without manual configuration.
  2. **100% Permissive MIT License**: Zero AGPL restrictions; clean modular architecture suitable for enterprise embedding.
  3. **Instant Zero-Install Fallback Mode**: Ships with a fast procedural generative synthesis engine so developers can run, test, and develop UI/API pipelines immediately on any CPU without waiting for multi-gigabyte weight downloads.
  4. **Built-In Prompt Optimizer**: Enriches sparse user prompts with artistic composition, volumetric lighting, and detail modifiers.
  5. **Dual Terminal CLI + Embedded Web Studio**: Provides both a rich CLI and an embedded glassmorphism web studio with zero heavy frontend build steps.

---

## 3. Architecture & Tech Stack

```
               User Prompt & Generation Settings
                               │
                               ▼
                ┌─────────────────────────────┐
                │   Prompt Optimization Engine│
                │   - Quality modifiers       │
                │   - Negative prompt expander│
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │  Hardware Profiler          │
                │  - Probes CUDA VRAM & cores │
                │  - Selects FP16 / FP32      │
                │  - Configures CPU fallback  │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │  Diffusers Generation Core  │
                │  - Hardware-tuned pipeline  │
                │  - Latent sampling & steps  │
                │  - Seed & reproducibility   │
                └──────────────┬──────────────┘
                               │
                               ▼
                ┌─────────────────────────────┐
                │   PNG & Metadata Exporter   │
                │   - Embedded generation meta│
                │   - Hardware performance log│
                └─────────────────────────────┘
```

- **Runtime**: Python 3.10+
- **Core Dependencies**: `Pillow`, `numpy`, `pydantic`
- **Optional Accelerators**: `torch`, `diffusers`, `accelerate`

---

## 4. File Structure

```
hardware-aware-diffusers-studio/
├── PLAN.md
├── DEVLOG.md
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── Dockerfile
├── pyproject.toml
├── .gitignore
├── .env.example
├── .github/
│   ├── workflows/ci.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── fixtures/
│   └── sample_prompt.json
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── hardware.py
│   ├── optimizer.py
│   ├── generator.py
│   ├── studio.py
│   └── cli.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_generator.py
    ├── test_hardware.py
    ├── test_models.py
    ├── test_optimizer.py
    └── test_studio.py
```
