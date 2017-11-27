from sanic import Sanic, Blueprint
from sanic.response import json
from sanic.exceptions import NotFound, ServerError

from ezq_query_api.routes import rest_v1
from ezq_query_api.database import pool_connect

app = Sanic(__name__)
app.config.from_envvar('CONFIG')

app.blueprint(rest_v1, url_prefix='/api/query/rest/v1')

@app.exception(NotFound)
async def ignore_404s(request, exception):
    result = {
        'code': -1,
        'message': 'Not Found',
        'http_status': 404
    }
    return json(result, ensure_ascii=False, escape_forward_slashes=False)

@app.exception(ServerError)
async def ignore_500s(request, exception):
    result = {
        'code': -1,
        'message': 'Not Found',
        'http_status': 500
    }
    return json(result, ensure_ascii=False, escape_forward_slashes=False)

@app.listener('before_server_start')
async def connect_db(app, loop):
    await pool_connect(app.config.DB_CONNECT_URL)

app.run(
    host=app.config.HOST,
    port=app.config.PORT,
    debug=app.config.DEBUG
)
