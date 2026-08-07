from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlmodel import Session
from ..core.db import get_session
from ..schemas import DescribeResponse, DescribeBatchResponse, DescribeItemResponse
from ..services.describe_service import describe_and_persist
from ..core.config import settings
from typing import List

router = APIRouter()

@router.post("/describe", response_model=DescribeResponse)
async def describe_image_endpoint(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    project_id: int = Form(1),
    model: str = Form(settings.OPENAI_DEFAULT_MODEL),
    temperature: float = Form(0.2),
    max_tokens: int = Form(400),
    session: Session = Depends(get_session),
):
    if file.content_type not in ("image/png", "image/jpeg", "image/webp"):
        raise HTTPException(status_code=400, detail=f"Unsupported content type: {file.content_type}")

    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    res = await describe_and_persist(
        session=session,
        project_id=project_id,
        filename=file.filename or "upload",
        image_bytes=image_bytes,
        mime_type=file.content_type,
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return DescribeResponse(
        text=res.output_text or "",
        model=model,
        tokens_in=res.tokens_in,
        tokens_out=res.tokens_out,
    )

@router.post("/describe_batch", response_model=DescribeBatchResponse)
async def describe_batch(
    files: List[UploadFile] = File(...),
    prompt: str = Form(...),
    project_id: int = Form(1),
    model: str = Form(settings.OPENAI_DEFAULT_MODEL),
    temperature: float = Form(0.2),
    max_tokens: int = Form(400),
    session: Session = Depends(get_session),
):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    results: list[DescribeItemResponse] = []

    for file in files:
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(status_code=400, detail=f"Empty file: {file.filename}")

        # nutzt deine EXISTIERENDE Logik (wichtig: nicht duplizieren)
        res = await describe_and_persist(
            session=session,
            project_id=project_id,
            filename=file.filename or "upload",
            image_bytes=image_bytes,
            mime_type=file.content_type,
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        results.append(
            DescribeItemResponse(
                filename=file.filename or "upload",
                text=res.output_text or "",
                model=model,
                tokens_in=getattr(res, "tokens_in", None),
                tokens_out=getattr(res, "tokens_out", None),
            )
        )

    return DescribeBatchResponse(count=len(results), results=results)
