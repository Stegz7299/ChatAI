import os
from dotenv import load_dotenv
import aioredis
from rejson import Client

load_dotenv()

class Redis:
    def __init__(self):
        """Initialize connection settings."""
        self.REDIS_URL = os.environ['REDIS_URL']
        self.REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
        self.REDIS_USER = os.environ['REDIS_USER']
        self.REDIS_HOST = os.environ['REDIS_HOST']
        self.REDIS_PORT = os.environ['REDIS_PORT']
        self.connection_url = f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"

    async def create_connection(self):
        """Create and return aioredis connection."""
        return await aioredis.from_url(self.connection_url, decode_responses=True)

    def create_rejson_client(self):
        """Create and return a ReJSON client."""
        return Client(host=self.REDIS_HOST, port=self.REDIS_PORT, decode_responses=True, username=self.REDIS_USER, password=self.REDIS_PASSWORD)
