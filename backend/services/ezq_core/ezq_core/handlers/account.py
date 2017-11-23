from ezq_core.publisher import core_publish
import ezq_core.accessor as A

async def create_account(params):
    pass

async def delete_account(params):
    pass

async def update_account(params):
    result = await A.update_account(params)
    await core_publish({
        'event': 'UPDATE_ACCOUNT_DONE',
        'request_id': params['request_id']
    })
    return result
