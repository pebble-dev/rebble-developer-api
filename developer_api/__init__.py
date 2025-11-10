from flask import Flask, request
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from rws_common import honeycomb

from .settings import config
from .api import init_api
from .models import init_app

app = Flask(__name__)
cors = CORS(app)
app.config.update(**config)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

honeycomb.init(app, 'developer_api')
honeycomb.sample_routes['api.sync'] = 10

init_app(app)
init_api(app)

@app.route('/heartbeat')
@app.route('/developer_api/heartbeat')
def heartbeat():
    return 'ok'
