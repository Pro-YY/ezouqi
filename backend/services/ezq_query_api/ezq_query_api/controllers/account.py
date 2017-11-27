import ezq_query_api.accessors as A

async def get_account_by_id(account_id, *args, **kwargs):
    result = await A.fetch_account_by_id(account_id, [])
    return result

async def list_account(*args, **kwargs):
    result = await A.query_account([])
    return result
