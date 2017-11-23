import asyncio
import uvloop
import os
import signal
import functools

from ezq_core.config import config
from ezq_core.database import pool_connect
from ezq_core.subscriber import start_subscribe
from ezq_core.publisher import config as publisher_config
from ezq_core.logger import logger

def on_exit(loop, signame):
    logger.info('got signal {}: exit'.format(signame))
    loop.stop()

def main():
    asyncio.set_event_loop(uvloop.new_event_loop())
    loop = asyncio.get_event_loop()

    config.from_file(os.environ['CONFIG'])

    # postgres connection pool
    loop.create_task(pool_connect(config.DB_CONNECT_URL))
    # rabbitmq subscriber
    loop.create_task(start_subscribe(config.MQ_CONNECT_URL))
    # rabbitmq publisher
    loop.create_task(publisher_config(config.MQ_CONNECT_URL))

    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                functools.partial(on_exit, loop, signame))

    try:
        loop.run_forever()
    except Exception as e:
        logger.error(e)
        loop.stop()
    finally:
        loop.stop()

if __name__ == '__main__':
    main()
