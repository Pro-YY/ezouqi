import asyncpg

from ezq_core.logger import logger

_POOL = None

async def pool_connect(url, *args, **kwargs):
    global _POOL
    _POOL = await asyncpg.create_pool(url)
    logger.info('postgress connected')

async def raw_exec(scmd, *sarg):
    async with _POOL.acquire() as conn:
        return await conn.execute(scmd, *sarg)
