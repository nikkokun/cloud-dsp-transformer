from sanic import Sanic
from sanic.response import json
from sanic.log import logger
from sanic.response import text
# import myapp.default_settings

app = Sanic()

db_settings = {
    'DB_HOST': 'localhost',
    'DB_NAME': 'appdb',
    'DB_USER': 'appuser'
}

app.config.update(db_settings)
# app.config.from_object(myapp.default_settings)


@app.route('/get', methods=['GET'])
async def get_handler(request):
	return text('GET request - {}'.format(request.args))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
