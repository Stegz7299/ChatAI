class StreamConsumer:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.last_ids = {}

    async def consume_stream(self, count: int, block: int, stream_channel: str):
        try:
            # Use '$' so it reads only new messages
            last_id = self.last_ids.get(stream_channel, '$')

            response = await self.redis_client.xread(
                streams={stream_channel: last_id}, count=count, block=20000
            )

            if response:
                for stream, messages in response:
                    if messages:
                        self.last_ids[stream_channel] = messages[-1][0]
                return response
        except Exception as e:
            print(f"Error consuming from stream => {e}")

    async def delete_message(self, stream_channel: str, message_id: str):
        try:
            await self.redis_client.xdel(stream_channel, message_id)
            print(f"Message id {message_id} deleted from {stream_channel} stream")
        except Exception as e:
            print(f"Error deleting message from stream => {e}")
