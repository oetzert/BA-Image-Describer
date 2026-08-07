import hashlib
import os
from sqlmodel import Session
from ..core.config import settings
from ..models import Image, Run, Result
from .providers.openai_provider import OpenAIProvider
from datetime import datetime, timezone
from .json_store import JsonResultRecord, append_record

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ensure_upload_dir():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

async def describe_and_persist(
    session: Session,
    project_id: int,
    filename: str,
    image_bytes: bytes,
    mime_type: str,
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
) -> Result:
    ensure_upload_dir()
    digest = sha256_bytes(image_bytes)
    storage_path = os.path.join(settings.UPLOAD_DIR, f"{digest}_{filename}")

    # store image file
    with open(storage_path, "wb") as f:
        f.write(image_bytes)

    img = Image(
        project_id=project_id,
        filename=filename,
        storage_path=storage_path,
        sha256=digest,
    )
    session.add(img)
    session.commit()
    session.refresh(img)

    run = Run(
        project_id=project_id,
        model=model,
        prompt=prompt,
        params_json=f'{{"temperature": {temperature}, "max_tokens": {max_tokens}}}',
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    provider = OpenAIProvider()
    out = await provider.describe_image(
        image_bytes=image_bytes,
        prompt=prompt,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        mime_type=mime_type,
    )

    res = Result(
        run_id=run.id,
        image_id=img.id,
        status="done",
        output_text=out["text"],
        tokens_in=out.get("tokens_in"),
        tokens_out=out.get("tokens_out"),
    )
    session.add(res)
    session.commit()
    session.refresh(res)

    created_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    record = JsonResultRecord(
        project_id=project_id,
        image_id=img.id,
        run_id=run.id,
        filename=filename,
        sha256=digest,
        storage_path=storage_path,
        prompt=prompt,
        model=model,
        params={"temperature": temperature, "max_tokens": max_tokens},
        output_text=res.output_text or "",
        tokens_in=res.tokens_in,
        tokens_out=res.tokens_out,
        created_at=created_at,
    )
    append_record(project_id, record)


    return res
