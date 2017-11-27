from json import dumps
from sanic import Blueprint
from sanic.response import HTTPResponse

import ezq_query_api.controllers as C
from .helpers.json_serialize import serialize

rest_v1 = Blueprint('rest_v1')

def _make_response(result):
    return HTTPResponse(dumps(result, default=serialize),
            status=200, headers=None, content_type='application/json')

async def _account_uuid(request, account_id):
    result = await C.get_account_by_id(account_id)
    return _make_response(result)

async def _account_root(request):
    result = await C.list_account()
    return HTTPResponse(dumps(result, default=serialize),
            status=200, headers=None, content_type='application/json')

rest_v1.add_route(_account_uuid,
        '/account/<account_id:string>', methods=['GET'])

rest_v1.add_route(_account_root,
        '/account', methods=['GET'])
