import asyncpg

from ezq_core.logger import logger

_POOL = None

async def pool_connect(url, *args, **kwargs):
    global _POOL
    _POOL = await asyncpg.create_pool(url)
    logger.info('postgress connected')

async def sql():
    global _POOL
    async with _POOL.acquire() as conn:
        #row = await conn.fetchrow(
        #    'SELECT * FROM users WHERE name = $1', 'Bob')
        row = await conn.fetch(
            'SELECT * FROM users')
        return row
