from ezq_command_api.publisher import publish

async def create_account(req, *args, **kwargs):
    request_json = req.json
    msg = {
        'request_id': req.headers['x-request-id'],
        'command': 'CREATE_ACCOUNT',
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result

async def update_account(req, account_id, *args, **kwargs):
    print(req.headers['x-request-id'])
    request_json = req.json
    msg = {
        'request_id': req.headers['x-request-id'],
        'command': 'UPDATE_ACCOUNT',
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result

async def delete_account(req, account_id, *args, **kwargs):
    msg = {
        'request_id': req.headers['x-request-id'],
        'command': 'DELETE_ACCOUNT',
        'request_json': req.json
    }
    await publish(msg)
    result = msg
    return result
