import os
import json
import aiofiles
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from ..redis.config import Redis
from uuid import uuid4
from utils import file_reader  # ✅ make sure this import works

files = APIRouter()
redis = Redis()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@files.post("/upload_file")
async def upload_file(token: str = Form(...), file: UploadFile = File(...)):
    redis_client = await redis.create_connection()

    exists = await redis_client.exists(token)
    if not exists:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    # Save the file to disk
    file_id = uuid4().hex
    safe_filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # ✅ Extract text using file_reader
    extracted_text = file_reader.read_file(file_path)

    meta = {
        "filename": file.filename,
        "path": file_path,
        "size": len(content),
        "content_preview": extracted_text[:500],  # first 500 chars
    }

    # ✅ Store metadata in Redis
    await redis_client.rpush(f"{token}:files", json.dumps(meta))

    # ✅ Push extracted content into message stream so the model “sees” it
    await redis_client.xadd(
        name="message_channel",
        fields={token: f"File uploaded: {file.filename}\n\nExtracted content:\n{extracted_text[:1000]}"}
    )

    return {
        "status": "uploaded",
        "filename": file.filename,
        "path": file_path,
        "message": f"File uploaded and extracted: {file.filename}",
        "preview": extracted_text[:300]
    }
