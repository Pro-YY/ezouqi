from ezq_command_api.publisher import publish

async def create_account(req, *args, **kwargs):
    request_json = req.json
    msg = {
        'event': 'CREATE_ACCOUNT_INIT',
        'request_id': req.headers['x-request-id'],
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result

async def update_account(req, account_id, *args, **kwargs):
    print(req.headers['x-request-id'])
    request_json = req.json
    msg = {
        'event': 'UPDATE_ACCOUNT_INIT',
        'account_id': account_id,
        'request_id': req.headers['x-request-id'],
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result

async def delete_account(req, account_id, *args, **kwargs):
    msg = {
        'event': 'DELETE_ACCOUNT_INIT',
        'request_id': req.headers['x-request-id'],
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result
