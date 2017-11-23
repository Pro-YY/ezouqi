import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from ujson import loads

from ezq_core.dispatcher import dispatch
from ezq_core.logger import logger

async def on_message(message: IncomingMessage):
    with message.process():     # auto message.ack()
        body = loads(message.body)
        event = body['event']
        print('# {} [received] sleep 1 sec...'.format(event))
        await asyncio.sleep(1) # Represents async I/O operations
        del body['event']
        await dispatch(event, body)

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
