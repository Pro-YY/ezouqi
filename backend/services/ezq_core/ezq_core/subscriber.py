import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from ujson import loads

from ezq_core.handlers import switch
from ezq_core.logger import logger

async def on_message(message: IncomingMessage):
    with message.process():     # auto message.ack()
        sec = 2
        print("Before sleep! %s" % sec)
        await asyncio.sleep(sec) # Represents async I/O operations
        print("After sleep! %s" % sec)
        body = loads(message.body)
        await switch(body['command'], body)

async def start_subscribe(url, *args, **kwargs):
    connection = await connect_robust(url)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=20)

    exchange = await channel.declare_exchange(
            'ezq_exchange',
            ExchangeType.DIRECT
    )
    queue = await channel.declare_queue(
            'ezq_core_queue',
            exclusive=False,
            durable=True
    )
    await queue.bind(exchange, routing_key='ezq_core_queue_key')

    await queue.consume(on_message)
    logger.info('rabbitmq connected and started subscribing...')
