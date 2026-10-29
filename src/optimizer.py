from typing import Tuple, Optional

class PromptOptimizer:
    """Enhances basic prompts with photographic modifiers and standardizes negative prompts."""

    QUALITY_MODIFIERS = [
        "highly detailed",
        "photorealistic",
        "8k resolution",
        "cinematic lighting",
        "octane render",
        "volumetric atmosphere",
        "fine textures",
    ]

    DEFAULT_NEGATIVE = (
        "blurry, low resolution, bad anatomy, distorted hands, watermark, "
        "grainy, duplicate, cropped, out of frame, signature, text, jpeg artifacts"
    )

    @classmethod
    def optimize(cls, prompt: str, style: str = "photorealistic") -> Tuple[str, str]:
        """Enrich a prompt and ensure negative prompt coverage."""
        clean_prompt = prompt.strip().rstrip(".")
        if not clean_prompt:
            return "abstract geometric art, 8k resolution, masterpiece", cls.DEFAULT_NEGATIVE

        # Avoid duplicating existing quality terms
        lower = clean_prompt.lower()
        added_mods = [m for m in cls.QUALITY_MODIFIERS if m not in lower]

        if style == "photorealistic":
            selected_mods = added_mods[:4]
        else:
            selected_mods = ["digital illustration", "artstation trending", "vibrant color palette"]

        enhanced_prompt = f"{clean_prompt}, {', '.join(selected_mods)}"
        return enhanced_prompt, cls.DEFAULT_NEGATIVE
