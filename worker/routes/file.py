from fastapi import APIRouter, UploadFile, File, Form
from src.schema.file_handler import FileHandler
from src.redis.config import Redis
from src.redis.cache import Cache
from rejson import Path

file_router = APIRouter()
redis = Redis()

@file_router.post("/upload")
async def upload_file(token: str = Form(...), file: UploadFile = File(...)):
    handler = FileHandler()
    filepath = handler.save_file(file, token)

    json_client = redis.create_rejson_connection()
    cache = Cache(json_client)

    await cache.add_message_to_cache(
        token=token,
        source="file",
        message_data={"msg": filepath}
    )

    return {"status": "ok", "filename": filepath}