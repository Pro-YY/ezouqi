from sanic import Sanic
from sanic.response import json
from sanic.exceptions import NotFound, ServerError
from uuid import uuid4

from ezq_command_api.routes import rest_v1 as routes_rest_v1
from ezq_command_api.publisher import config as publisher_config

app = Sanic(__name__)
app.config.from_envvar('CONFIG')

# mount middlewares
# NOTE: middleware only work with app, not blueprint specific
@app.middleware('request')
async def add_x_request_id_middlware(request):
    request.headers['x-request-id'] = str(uuid4())

# mount all blueprints
app.blueprint(routes_rest_v1, url_prefix='/api/command/rest/v1')

# error handlers
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
    print(exception);
    result = {
        'code': -1,
        'message': 'Server Error',
        'http_status': 500
    }
    return json(result, ensure_ascii=False, escape_forward_slashes=False)

@app.listener('before_server_start')
async def publisher_init(app, loop):
    await publisher_config(app.config.MQ_CONNECT_URL)
    print('server is about to start...')

# run server
app.run(
    host=app.config.HOST,
    port=app.config.PORT,
    debug=app.config.DEBUG
)
