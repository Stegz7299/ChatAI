import asyncio
from src.model.gptj import GPTChat
from src.redis.cache import Cache
from src.redis.config import Redis
from src.redis.stream import StreamConsumer
import os
import json
from dotenv import load_dotenv
from src.schema.chat import Message
from src.redis.producer import Producer

# Load .env file
load_dotenv()

redis = Redis()

async def main():
    json_client = redis.create_rejson_connection()
    redis_client = await redis.create_connection()
    consumer = StreamConsumer(redis_client)
    cache = Cache(json_client)
    producer = Producer(redis_client)

    print("Stream consumer started")
    print("Stream waiting for new messages")

    while True:
        response = await consumer.consume_stream(stream_channel="message_channel", count=1, block=0)

        if response:
            for stream, messages in response:
                for message in messages:
                    message_id = message[0]
                    token = [k.decode('utf-8') for k, v in message[1].items()][0]
                    message = [v.decode('utf-8') for k, v in message[1].items()][0]

                    msg = Message(msg=message)
                    await cache.add_message_to_cache(token=token, source="human", message_data=msg.dict())

                    data = await cache.get_chat_history(token=token)
                    message_data = data['messages'][-4:]

                    chat_messages = []
                    for i in message_data:
                        role = "user" if i.get("source", "human") == "human" else "assistant"
                        chat_messages.append({
                            "role": role,
                            "content": i["msg"]
                        })

                    res = GPTChat().query(messages=chat_messages)
                    msg = Message(msg=res)

                    stream_data = {str(token): json.dumps(msg.dict())}
                    await producer.add_to_stream(stream_data, "response_channel")

                    await cache.add_message_to_cache(token=token, source="bot", message_data=msg.dict())

                await consumer.delete_message(stream_channel="message_channel", message_id=message_id)

if __name__ == "__main__":
    asyncio.run(main())
