from abc import ABC, abstractmethod

class VisionProvider(ABC):
    @abstractmethod
    async def describe_image(
        self,
        image_bytes: bytes,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        """Return dict: {text, tokens_in, tokens_out, raw}"""
        raise NotImplementedError
