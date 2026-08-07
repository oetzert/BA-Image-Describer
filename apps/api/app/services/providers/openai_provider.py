import base64
from openai import AsyncOpenAI
from ...core.config import settings
from .base import VisionProvider

class OpenAIProvider(VisionProvider):
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY missing in .env")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def _to_data_url(self, image_bytes: bytes, mime_type: str) -> str:
        """Convert raw image bytes to a data: URL usable by the Responses API."""
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"

    async def count_input_tokens(
        self,
        *,
        prompt: str,
        model: str,
        image_bytes: bytes | None = None,
        mime_type: str | None = None,
        instructions: str | None = None,
    ) -> int:
        """Return input token count for a would-be /responses request.

        Mirrors the OpenAI endpoint POST /v1/responses/input_tokens.
        """

        if image_bytes is not None and mime_type is not None:
            input_payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": self._to_data_url(image_bytes, mime_type),
                        },
                    ],
                }
            ]
        else:
            input_payload = prompt

        resp = await self.client.responses.input_tokens.count(
            model=model,
            input=input_payload,
            instructions=instructions,
        )
        return int(resp.input_tokens)

    async def describe_image(
        self,
        image_bytes: bytes,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
        mime_type: str = "image/png",
    ) -> dict:
        # NOTE: This uses the Responses API shape; adapt if you prefer Chat Completions.
        resp = await self.client.responses.create(
            model=model,
            input=[{
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": self._to_data_url(image_bytes, mime_type)},
                ],
            }],
            temperature=temperature,
            max_output_tokens=max_tokens,
        )

        # Extract text (robustly)
        text_parts = []
        for item in resp.output:
            if item.type == "message":
                for c in item.content:
                    if c.type == "output_text":
                        text_parts.append(c.text)

        usage = getattr(resp, "usage", None)
        tokens_in = getattr(usage, "input_tokens", None) if usage else None
        tokens_out = getattr(usage, "output_tokens", None) if usage else None

        return {
            "text": "\n".join(text_parts).strip() or "(no text returned)",
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "raw": resp.model_dump(),
        }
