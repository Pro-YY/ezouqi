from sanic import Blueprint
from sanic.response import json

rest_v1 = Blueprint('rest_v1')

@rest_v1.route('/account/<account_id:string>', methods=['GET'])
async def get_account_handler(request, account_id):
    print(request.scheme)
    print(request.token)

    url = request.app.url_for('rest_v1.get_account_handler',
            account_id=account_id, _external=True,
            _scheme=request.app.config.EXTERNAL_SCHEME,
            _server=request.app.config.EXTERNAL_SERVER
    )
    account_obj = {
        'mock': True,
        'name': '杨阳',
        'email': 'this.pro-yy.com <script>'
    }
    result = { 'id': account_id, 'j': account_obj, 'url': url }
    return json(result, ensure_ascii=False, escape_forward_slashes=False)

@rest_v1.route('/party/<party_id:string>', methods=['GET'])
async def get_party_handler(request, party_id):
    url = request.app.url_for('rest_v1.get_party_handler',
            party_id=party_id, _external=True,
            _scheme=request.app.config.EXTERNAL_SCHEME,
            _server=request.app.config.EXTERNAL_SERVER
    )
    party_obj = {
        'mock': True,
        'name': '小聚会',
    }
    result = { 'id': party_id, 'j': party_obj, 'url': url }
    return json(result, ensure_ascii=False, escape_forward_slashes=False)
