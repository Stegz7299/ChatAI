# server/routes/history.py
from fastapi import APIRouter, Query, HTTPException
from ..redis.config import Redis
from ..redis.cache import Cache

history_router = APIRouter()
redis_instance = Redis()

@history_router.get("/chat/history")
async def get_chat_history(token: str = Query(...)):
    json_client = redis_instance.create_rejson_client()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)

    if not data or "messages" not in data:
        raise HTTPException(status_code=404, detail="No chat history found")

    return {"history": data["messages"]}

@history_router.get("/chat/tokens")
async def get_all_tokens():
    json_client = redis_instance.create_rejson_client()
    keys = await json_client.keys("*")  # adjust if your keys have a prefix
    return {"tokens": keys}
