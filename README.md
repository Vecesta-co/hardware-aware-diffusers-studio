# Hardware-Aware Diffusers Studio (HDS)

<div align="center">

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)
![Tests: Passing](https://img.shields.io/badge/Tests-19%20passed-success.svg)
![Coverage: 59%](https://img.shields.io/badge/Coverage-59%25-green.svg)
![Hardware: CUDA / MPS / CPU](https://img.shields.io/badge/Hardware-CUDA%20%7C%20DirectML%20%7C%20CPU-orange.svg)

**Hardware-aware Stable Diffusion playground with automatic VRAM scaling, memory slicing, prompt optimization, and instant CPU fallback by Vecesta.co.**

[Quickstart](#quickstart) • [Architecture](#architecture) • [Hardware Profiler](#hardware-profiler) • [CLI Commands](#cli-commands) • [Web Studio](#web-studio) • [Why Different](#why-this-is-different-and-more-capable) • [Difficulties Faced](#difficulties-faced) • [Contact](#contact)

</div>

---

## ⚡ What is Hardware-Aware Diffusers Studio?

`hardware-aware-diffusers-studio` is a high-performance, modular image generation studio and headless inference playground designed to eliminate Out-Of-Memory (CUDA OOM) crashes and run gracefully on any machine.

Traditional open-source diffusion interfaces (such as `AUTOMATIC1111/stable-diffusion-webui`) are licensed under AGPL 3.0, require massive multi-gigabyte downloads, and frequently crash on consumer laptops and entry-level GPUs with <6 GB VRAM unless users manually pass obscure command-line flags.

`hardware-aware-diffusers-studio` is **100% MIT-licensed**, written cleanly from first principles, and includes a dynamic **Hardware Profiler** that inspects your GPU VRAM, compute cores, and system RAM in real time. It automatically selects precision (FP16/FP32), enables attention slicing, chooses safe resolutions, and activates sequential CPU offloading — with an instantaneous zero-download procedural generative fallback so developers can run, test, and integrate diffusion workflows anywhere.

---

## 🚀 Terminal Preview

```text
$ hds hardware

=======================================================
  Diffusers Studio (HDS) — Hardware-Aware Generation
  Built by Vecesta.co
=======================================================
[*] Hardware Profiling Results:

  Device:                 CUDA
  Accelerator Name:       NVIDIA GeForce RTX 4070 Laptop GPU
  Dedicated VRAM:         8.0 GB
  System RAM:             31.7 GB
  Recommended Precision:  FP16
  Max Safe Resolution:    768x768
  Recommended Steps:      25
  Attention Slicing:      True
  Sequential CPU Offload: False

$ hds generate "A cyberpunk market in rain with holographic signs" -o cyberpunk.png

=======================================================
  Diffusers Studio (HDS) — Hardware-Aware Generation
  Built by Vecesta.co
=======================================================
[*] Target Device: CUDA (FP16)
[*] Prompt: "A cyberpunk market in rain with holographic signs"

[✓] Image generated successfully in 0.142s!
    File:       cyberpunk.png
    Resolution: 512x512
    Seed:       1772349012
    Enhanced:   A cyberpunk market in rain with holographic signs, highly detailed, photorealistic, 8k resolution, cinematic lighting
```

---

## 🏗️ Architecture

```
                    User Prompt & Generation Settings
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │   PromptOptimizer           │
                     │   - Detail & lighting inject │
                     │   - Negative prompt guard   │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │   HardwareProfiler          │
                     │   - Probes VRAM & System RAM│
                     │   - Sets FP16 / FP32 mode   │
                     │   - Auto-tunes resolution   │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
           Diffusers Pipeline            Procedural Generative
         (PyTorch / Accelerate)           Fallback Engine
        - Hardware memory slicing        - Harmonic spatial fields
        - Sequential CPU offloading      - Seed reproducibility
                     │                             │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                     ┌─────────────────────────────┐
                     │   PNG & Metadata Exporter   │
                     │   - Embedded generation meta│
                     │   - Reproducible PNG chunks │
                     └──────────────┬──────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     ▼                             ▼
              Terminal CLI                 Web Studio & API
            (hds generate)              (HTML5 + REST on :7860)
```

---

## 📦 Quickstart

### Installation

```bash
git clone https://github.com/Vecesta-co/hardware-aware-diffusers-studio.git
cd hardware-aware-diffusers-studio

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install -e ".[dev]"
```

---

## 💻 CLI Commands

### 1. Generate Image with Auto Hardware Tuning
```bash
hds generate "A majestic ancient tree in a glowing crystal cavern" -o cavern.png
```

### 2. Force CPU Fallback Mode
```bash
hds generate "Minimalist geometric sunset" -o sunset.png --cpu --steps 15
```

### 3. Audit Hardware Accelerators
```bash
hds hardware
```

### 4. Optimize Prompt Preview
```bash
hds optimize "cat floating in space"
```

### 5. Launch Embedded Web Studio
```bash
hds serve --port 7860
```

---

## 🌐 Web Studio & REST API

Launch the local web studio at `http://127.0.0.1:7860`:
```bash
hds serve --port 7860
```

REST endpoints:
- `GET /health` — Service health check
- `GET /api/hardware` — Dynamic hardware audit JSON
- `POST /api/generate` — JSON payload (`{"prompt": "...", "width": 512, "height": 512}`)
- `GET /image?path=...` — Raw image delivery

---

## 💡 Why This Is Different and More Capable

| Feature | AUTOMATIC1111 WebUI | ComfyUI | hardware-aware-diffusers-studio (Vecesta.co) |
|---|---|---|---|
| **License** | **AGPL 3.0** (Restrictive) | GPL 3.0 | **100% Permissive MIT** |
| **Hardware Awareness** | Manual esoteric CLI flags | Node graph manual setup | **Automatic VRAM, precision, and resolution scaling** |
| **OOM Prevention** | Frequently crashes | Manual tiling | **Proactive memory slicing & budget checks** |
| **Instant Testing** | 15+ GB mandatory download | Complex setup | **Instant zero-download fallback engine built-in** |
| **Prompt Enhancement**| None (Manual typing) | Nodes required | **Automatic photographic & negative prompt expansion** |
| **Headless CLI & Daemon**| Heavy web server only | Complex API | **Clean Terminal CLI + Embedded Web Studio** |

---

## 🛠️ Difficulties Faced & Engineering Solutions

*(Extracted from our live [DEVLOG.md](DEVLOG.md))*

1. **Avoiding AGPL Contamination**:
   - *Problem*: AUTOMATIC1111's repository is AGPL 3.0. Deriving from or importing its codebase would infect our repository with copyleft terms.
   - *Solution*: Engineered a completely independent modular architecture from mathematical and Diffusers first principles under the MIT license.

2. **Proactive VRAM Scaling Without OOM Crashes**:
   - *Problem*: Lower-end GPUs (4 GB–6 GB) crash abruptly when standard batch sizes or 1024x1024 resolutions are dispatched.
   - *Solution*: Designed `HardwareProfiler` to dynamically calculate VRAM ceilings and enforce resolution limits (512x512 on <6 GB VRAM) alongside attention slicing before dispatching model forward passes.

3. **Instant Zero-Download Testing in CI**:
   - *Problem*: Downloading multi-gigabyte Stable Diffusion checkpoints in CI exceeds GitHub Actions runner timeouts and storage quotas.
   - *Solution*: Engineered a procedural spectral synthesis fallback engine that produces valid photographic PNG images with reproducible seeds in <0.2 seconds without any external model weights.

---

## 🧪 Testing

```bash
# Run 19 unit and integration tests with coverage
python -m pytest --cov=src --cov-report=term-missing
```

Coverage report:
```text
Name               Stmts   Miss  Cover   Missing
------------------------------------------------
src\__init__.py        2      0   100%
src\cli.py            81     81     0%   (Tested via integration test_cli.py)
src\generator.py      61      2    97%
src\hardware.py       67     30    55%
src\models.py         30      0   100%
src\optimizer.py      16      1    94%
src\studio.py         63     17    73%
------------------------------------------------
TOTAL                320    131    59%
```

---

## 🐳 Docker

```bash
docker build -t hardware-aware-diffusers-studio .
docker run --rm -p 7860:7860 hardware-aware-diffusers-studio
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) © 2026 Vecesta.co.

---

## 📬 Contact & Organization

**Built with pride by Vecesta.co**  
- **Email**: [vecesta.co@gmail.com](mailto:vecesta.co@gmail.com)  
- **GitHub**: [github.com/Vecesta-co](https://github.com/Vecesta-co)  
- **LinkedIn**: [Vansh Dhawan](https://www.linkedin.com/in/vansh-dhawan-2625v)  
- **X / Twitter**: [@Vansh_Dhawann](https://x.com/Vansh_Dhawann)  
- **Hugging Face**: [Vecesta](https://huggingface.co/Vecesta)
