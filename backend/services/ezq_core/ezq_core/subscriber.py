import asyncio
from aio_pika import connect_robust, IncomingMessage, ExchangeType
from ujson import loads

from ezq_core.dispatcher import dispatch
from ezq_core.logger import logger

async def on_message(message: IncomingMessage):
    print(message.body)
    body = loads(message.body)
    event = body['event']
    #print('# {} [received]'.format(event))
    print('# {} [received] sleep 1 sec..'.format(event))
    await asyncio.sleep(1) # Represents async I/O operations
    del body['event']
    await dispatch(event, body)
    # manual ack here
    # not with message.process() context, which auto ack even when error
    message.ack()

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
    # await queue.bind(exchange, routing_key='ezq_core_queue')
    await queue.bind(exchange) # default routing key is same as queue name

    await queue.consume(on_message)
    logger.info('rabbitmq connected and started subscribing...')
