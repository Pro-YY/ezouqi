import asyncpg
from collections import OrderedDict

_POOL = None

async def pool_connect(url, *args, **kwargs):
    global _POOL
    _POOL = await asyncpg.create_pool(url)
    print('postgress connected')

# No write operation for query api
#async def execute(scmd, *sarg):
#    async with _POOL.acquire() as conn:
#        return await conn.execute(scmd, *sarg)

async def fetchrow(scmd, *sarg):
    async with _POOL.acquire() as conn:
        record = await conn.fetchrow(scmd, *sarg)
        return OrderedDict(record)

async def fetch(scmd, *sarg):
    async with _POOL.acquire() as conn:
        records = await conn.fetch(scmd, *sarg)
        return list(map(lambda x: OrderedDict(x), records))
