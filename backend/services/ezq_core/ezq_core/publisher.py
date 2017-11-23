import asyncio
from aio_pika import connect_robust, Message, ExchangeType
from ujson import dumps

_CONNECT_URL = None

async def config(url):
    global _CONNECT_URL
    _CONNECT_URL = url

async def _publish(key, msg, *args, **kwargs):
    connection = await connect_robust(_CONNECT_URL)
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
                'ezq_exchange', ExchangeType.DIRECT)
        await channel.default_exchange.publish(
                Message(body=dumps(msg).encode()),
                routing_key=key
        )

async def core_publish(msg, *args, **kwargs):
    return await _publish('ezq_core_queue', msg, *args, **kwargs);
