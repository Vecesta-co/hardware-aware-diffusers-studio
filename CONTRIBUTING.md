# Contributing to Hardware-Aware Diffusers Studio

Thank you for contributing!

## Development Setup
```bash
git clone https://github.com/Vecesta-co/hardware-aware-diffusers-studio
cd hardware-aware-diffusers-studio
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest --cov=src
```
