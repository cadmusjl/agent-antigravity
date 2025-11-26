import replicate
from config import settings
from typing import Optional


class ImageCreationTool:
    """Tool for generating AI images using Replicate and Stable Diffusion"""

    def __init__(self):
        if settings.REPLICATE_API_TOKEN:
            replicate.api_key = settings.REPLICATE_API_TOKEN

    async def generate_image(
        self,
        prompt: str,
        style: str = "realistic",
        model: str = "stable-diffusion"
    ) -> str:
        """Generate an image using AI"""

        # Enhance prompt based on style
        style_modifiers = {
            "realistic": "photorealistic, 8k, highly detailed",
            "artistic": "artistic, creative, expressive",
            "minimalist": "minimalist, clean, simple",
            "vibrant": "vibrant colors, dynamic, energetic",
            "professional": "professional, clean, corporate"
        }

        enhanced_prompt = f"{prompt}, {style_modifiers.get(style, '')}"

        try:
            if model == "stable-diffusion":
                # Using Stable Diffusion XL
                output = await replicate.async_run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={
                        "prompt": enhanced_prompt,
                        "negative_prompt": "ugly, blurry, low quality",
                        "width": 1024,
                        "height": 1024,
                        "num_outputs": 1
                    }
                )
                return output[0] if output else None

            elif model == "dall-e":
                # Using DALL-E 3 via OpenAI
                import openai
                if settings.OPENAI_API_KEY:
                    openai.api_key = settings.OPENAI_API_KEY
                    response = await openai.images.generate(
                        model="dall-e-3",
                        prompt=enhanced_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1
                    )
                    return response.data[0].url
                else:
                    raise Exception("OpenAI API key required for DALL-E")

            else:
                raise ValueError(f"Unknown model: {model}")

        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")

    async def generate_variations(
        self,
        image_url: str,
        count: int = 3
    ) -> list:
        """Generate variations of an existing image"""
        try:
            output = await replicate.async_run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "image": image_url,
                    "num_outputs": count
                }
            )
            return output
        except Exception as e:
            raise Exception(f"Variation generation failed: {str(e)}")
