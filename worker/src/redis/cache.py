from .config import Redis
from rejson import Path
import uuid
import redis

class Cache:
    def __init__(self, json_client):
        self.json_client = json_client

    async def clear_cache(self, token: str):
        """Hapus cache lama untuk token tertentu"""
        await self.json_client.delete(token)
        print(f"Cache cleared for token: {token}")

    async def get_chat_history(self, token: str):
        try:
            data = self.json_client.jsonget(str(token), Path.rootPath())
        except redis.exceptions.ResponseError:
            data = None
        return data

    async def add_message_to_cache(self, token: str, source: str, message_data: dict):
        if source == "human":
            message_data['msg'] = "Human: " + message_data['msg']
        elif source == "bot":
            message_data['msg'] = "Bot: " + message_data['msg']

        for key, value in message_data.items():
            if isinstance(value, uuid.UUID):
                message_data[key] = str(value)

        try:
            key_type = self.json_client.type(str(token))
            if key_type == 'none':
                self.json_client.jsonset(str(token), Path.rootPath(), {"messages": []})
                print(f"New JSON object created for token: {token}")
            elif key_type in ['string', 'list', 'set', 'zset']:
                self.json_client.delete(str(token))
                self.json_client.jsonset(str(token), Path.rootPath(), {"messages": []})
                print(f"Cache cleared and reset for token: {token}")
        except redis.exceptions.ResponseError as e:
            print(f"Redis error: {e}")
            raise

        self.json_client.jsonarrappend(str(token), Path('.messages'), message_data)
        print(f"Message added to cache for token: {token}, message: {message_data}")
