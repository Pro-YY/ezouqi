import pika
from ujson import dumps

_CONNECT_URL = None

async def config(url):
    global _CONNECT_URL
    _CONNECT_URL = url

async def _publish(key, message, *args, **kwargs):
    global _CONNECT_URL
    parameters = pika.URLParameters(_CONNECT_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(
            exchange='ezq_exchange', exchange_type='direct')
    channel.basic_publish(
            exchange='ezq_exchange',
            routing_key=key,
            body=dumps(message))
    connection.close()

async def core_publish(msg, *args, **kwargs):
    return await _publish('ezq_core_queue', msg, *args, **kwargs);
