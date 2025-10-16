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

@history_router.get("/chat/history/{token}")
async def get_history_by_token(token:str):
    json_client = redis_instance.create_rejson_client()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)

    if not data or "messages" not in data:
        return {"messages: []"}
    

@history_router.get("/chat/tokens")
async def get_all_tokens():
    json_client = redis_instance.create_rejson_client()
    keys = json_client.keys("*")   # not async → no await
    return {"tokens": keys}

@history_router.delete("/chat/history")
async def delete_chat_history(token: str = Query(...)):
    json_client = redis_instance.create_rejson_client()
    key = token  # or f"history:{token}"
    exists = json_client.exists(key)
    if not exists:
        raise HTTPException(status_code=404, detail=f"No history found for token {token}")
    json_client.delete(key)
    return {"status": "deleted", "token": token}
