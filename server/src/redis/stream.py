class StreamConsumer:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    async def consume_stream(self, count: int, block: int, stream_channel: str):
        try:
            # Await the xread call
            response = await self.redis_client.xread(
                streams={stream_channel: '0'}, count=count, block=block
            )
            return response
        except Exception as e:
            print(f"Error consuming from stream => {e}")

    async def delete_message(self, stream_channel: str, message_id: str):
        try:
            # Await the xdel call
            await self.redis_client.xdel(stream_channel, message_id)
            print(f"Message id {message_id} deleted from {stream_channel} stream")
        except Exception as e:
            print(f"Error deleting message from stream => {e}")
