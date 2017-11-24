from sanic import Blueprint
from sanic.response import json, text

import ezq_command_api.controllers as C

rest_v1 = Blueprint('rest_v1')

# account routes
async def account_root(request):
    result = await C.create_account(request)
    return json(result, status=202)

async def account_uuid(request, account_id):
    if request.method == 'PUT':
        result = await C.update_account(request, account_id)
        return json(result, status=202)
    elif request.method == 'DELETE':
        result = await C.delete_account(request, account_id)
        return json(result, status=202)
    else:
        return json(None, status=405)

rest_v1.add_route(account_root,
        '/account',
        methods=['POST'])
rest_v1.add_route(account_uuid,
        '/account/<account_id:string>',
        methods=['PUT', 'DELETE'])

# weixin callback routes
async def weixin_miniprogram_callback(request):
    print(request.headers)
    print(request.raw_args)
    print(request.args)
    return text(request.args['echostr'][0])

rest_v1.add_route(weixin_miniprogram_callback,
        '/weixin/miniprogram-callback',
        methods=['GET', 'POST'])
