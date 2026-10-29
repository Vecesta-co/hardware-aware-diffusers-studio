import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
import os
from colorama import init, Fore, Style
from src.hardware import HardwareProfiler
from src.generator import DiffusersGenerator
from src.optimizer import PromptOptimizer
from src.models import GenerationRequest
from src.studio import run_studio

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}=======================================================
  Diffusers Studio (HDS) — Hardware-Aware Generation
  Built by Vecesta.co
======================================================={Style.RESET_ALL}"""
    print(banner)

def main():
    parser = argparse.ArgumentParser(
        prog="hardware-aware-diffusers-studio",
        description="Hardware-aware Stable Diffusion playground with automatic VRAM scaling and CPU fallback."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 1. Generate
    p_gen = subparsers.add_parser("generate", help="Generate image with hardware adaptation")
    p_gen.add_argument("prompt", help="Visual prompt description")
    p_gen.add_argument("--output", "-o", default="output.png", help="Output file path")
    p_gen.add_argument("--width", "-w", type=int, default=512, help="Image width")
    p_gen.add_argument("--height", "-H", type=int, default=512, help="Image height")
    p_gen.add_argument("--steps", "-s", type=int, default=20, help="Sampling steps")
    p_gen.add_argument("--seed", type=int, help="Random seed")
    p_gen.add_argument("--cpu", action="store_true", help="Force CPU fallback mode")
    p_gen.add_argument("--no-optimize", action="store_true", help="Disable prompt optimization")

    # 2. Hardware
    subparsers.add_parser("hardware", help="Audit hardware capabilities and recommended settings")

    # 3. Optimize
    p_opt = subparsers.add_parser("optimize", help="Preview prompt quality enhancement")
    p_opt.add_argument("prompt", help="Base prompt to enhance")

    # 4. Serve
    p_srv = subparsers.add_parser("serve", help="Launch local web studio")
    p_srv.add_argument("--port", "-p", type=int, default=7860, help="Web studio port")
    p_srv.add_argument("--host", default="127.0.0.1", help="Host address")

    args = parser.parse_args()

    if args.command == "hardware":
        print_banner()
        hw = HardwareProfiler.profile()
        print(f"{Fore.YELLOW}[*] Hardware Profiling Results:{Style.RESET_ALL}\n")
        print(f"  Device:                 {hw.device.upper()}")
        print(f"  Accelerator Name:       {hw.device_name}")
        print(f"  Dedicated VRAM:         {hw.vram_gb:.1f} GB")
        print(f"  System RAM:             {hw.ram_gb:.1f} GB")
        print(f"  Recommended Precision:  {hw.recommended_precision.upper()}")
        print(f"  Max Safe Resolution:    {hw.max_resolution}x{hw.max_resolution}")
        print(f"  Recommended Steps:      {hw.recommended_steps}")
        print(f"  Attention Slicing:      {hw.attention_slicing}")
        print(f"  Sequential CPU Offload: {hw.sequential_offload}")

    elif args.command == "optimize":
        print_banner()
        enhanced, neg = PromptOptimizer.optimize(args.prompt)
        print(f"{Fore.YELLOW}[*] Input Prompt:{Style.RESET_ALL}    {args.prompt}")
        print(f"{Fore.GREEN}[✓] Enhanced Prompt:{Style.RESET_ALL} {enhanced}")
        print(f"{Fore.CYAN}[ℹ] Negative Prompt:{Style.RESET_ALL} {neg}")

    elif args.command == "generate":
        print_banner()
        force = "cpu" if args.cpu else None
        hw = HardwareProfiler.profile(force_device=force)
        generator = DiffusersGenerator(hardware=hw)

        print(f"{Fore.YELLOW}[*] Target Device: {hw.device.upper()} ({hw.recommended_precision.upper()}){Style.RESET_ALL}")
        print(f"[*] Prompt: \"{args.prompt}\"")

        req = GenerationRequest(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            steps=args.steps,
            seed=args.seed,
            optimize_prompt=not args.no_optimize,
        )

        out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
        res = generator.generate(req, output_dir=out_dir)

        # Move to exact output path requested if different
        if res.output_path != args.output:
            if os.path.exists(args.output):
                os.remove(args.output)
            os.rename(res.output_path, args.output)

        print(f"\n{Fore.GREEN}[✓] Image generated successfully in {res.elapsed_seconds}s!{Style.RESET_ALL}")
        print(f"    File:       {args.output}")
        print(f"    Resolution: {res.width}x{res.height}")
        print(f"    Seed:       {res.seed}")
        print(f"    Enhanced:   {res.optimized_prompt}")

    elif args.command == "serve":
        print_banner()
        run_studio(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
