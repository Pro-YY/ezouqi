from ezq_core.database import sql

# TODO seperate logic from db access
async def create_account_handler(params):
    result = await sql()

async def update_account_handler(params):
    print(params)
    result = await sql()
    print(result)
    return result

async def delete_account_handler(params):
    result = await sql()

COMMANDS = {
    'CREATE_ACCOUNT': create_account_handler,
    'UPDATE_ACCOUNT': update_account_handler,
    'DELETE_ACCOUNT': delete_account_handler,
}

async def switch(command, params, *args, **kwargs):
    result = await COMMANDS[command](params)
    print('command done: {}'.format(command))
