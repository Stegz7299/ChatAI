import os
from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect, Depends, HTTPException
import uuid
from ..socket.connection import ConnectionManager
from ..socket.utils import get_token
from ..redis.producer import Producer
from ..redis.config import Redis
from ..redis.stream import StreamConsumer
from ..schema.chat import Chat
from ..redis.cache import Cache
import json
import logging

# Initialize router, connection manager, and Redis
chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# @route   POST /token
# @desc    Route to generate chat token
# @access  Public
@chat.post("/token")
async def token_generator(name: str, request: Request):
    token = str(uuid.uuid4())
    if name == "":
        raise HTTPException(status_code=400, detail={"loc": "name", "msg": "Enter a valid name"})

    # Create an async Redis connection
    redis_connection = await redis.create_connection()

    # Create new chat session
    chat_session = Chat(token=token, messages=[], name=name)

    # Store chat session as JSON string in Redis
    await redis_connection.set(str(token), json.dumps(chat_session.dict()))

    # Set a timeout for Redis data
    await redis_connection.expire(str(token), 3600)

    return chat_session.dict()

# @route   GET /refresh_token
# @desc    Route to refresh the chat session and return chat history
# @access  Public
@chat.get("/refresh_token")
async def refresh_token(request: Request, token: str):
    json_client = redis.create_rejson_connection()
    cache = Cache(json_client)
    data = await cache.get_chat_history(token)

    if data is None:
        # Jika tidak ada data untuk token ini, hapus cache lama jika ada
        await redis_client.delete(token)
        raise HTTPException(status_code=400, detail="Session expired or does not exist")

    return data


# @route   WebSocket /chat
# @desc    WebSocket for chatbot communication
# @access  Public
@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)
    json_client = redis.create_connection()
    consumer = StreamConsumer(redis_client)

    # Inisialisasi ulang dengan menghapus cache lama untuk token ini
    await redis_client.delete(token)  # Pastikan Redis cache untuk token ini dihapus

    try:
        while True:
            data = await websocket.receive_text()
            stream_data = {str(token): str(data)}
            logger.info(f"Sending message to message_channel: {stream_data}")
            await producer.add_to_stream(stream_data, "message_channel")

            # Provide count and block arguments
            response = await consumer.consume_stream(count=10, block=5000, stream_channel="response_channel")
            logger.info(f"Received response from response_channel: {response}")

            if response:
                if response:
                    for stream, messages in response:
                        for message in messages:
                            message_id = message[0]
                            data = message[1]

                            response_token = [k.decode() if isinstance(k, bytes) else k for k in data.keys()][0]
                            response_message = [v.decode() if isinstance(v, bytes) else v for v in data.values()][0]

                            logger.info(f"Processing message with token {response_token}")

                            if response_token == token:
                                logger.info(f"Sending response message: {response_message}")
                                await manager.send_personal_message(response_message, websocket)

                                # Only delete if it's the message we want
                                await consumer.delete_message(stream_channel="response_channel", message_id=message_id)
                                break  # Stop loop once response is sent


    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        manager.disconnect(websocket)
