from fastapi import APIRouter, File, UploadFile, Form, HTTPException

from ..core.config import settings
from ..services.providers.openai_provider import OpenAIProvider


router = APIRouter()


@router.post("/input_tokens")
async def input_tokens_endpoint(
    prompt: str = Form(...),
    model: str = Form(settings.OPENAI_DEFAULT_MODEL),
    instructions: str | None = Form(None),
    file: UploadFile | None = File(None),
):
    """Estimate input tokens for a would-be Responses API call.

    This mirrors OpenAI's POST /v1/responses/input_tokens behavior.
    """

    image_bytes = None
    mime_type = None

    if file is not None:
        if file.content_type not in ("image/png", "image/jpeg", "image/webp"):
            raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file")
        mime_type = file.content_type

    provider = OpenAIProvider()
    tokens = await provider.count_input_tokens(
        prompt=prompt,
        model=model,
        image_bytes=image_bytes,
        mime_type=mime_type,
        instructions=instructions,
    )

    return {"object": "response.input_tokens", "input_tokens": tokens}
