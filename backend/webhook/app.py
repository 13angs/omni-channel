import sys  
from pathlib import Path  
file = Path(__file__).resolve()
package_root_directory = file.parents [1]  
sys.path.append(str(package_root_directory))  

from flask_restful import Api
from flask import Flask
from line_api import LineApi
from dotenv import load_dotenv
import os
from werkzeug.middleware.proxy_fix import ProxyFix

# Load all env
load_dotenv('../.env')
DEBUG=bool(os.environ['DEBUG'])
DEV_PORT=int(os.environ['DEV_PORT'])


app = Flask(__name__)
api = Api(app)

api.add_resource(LineApi, '/webhook/v1/line/<int:client_id>')

# Tell Flask it is Behind a Proxy
if DEBUG == False:
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=DEV_PORT, debug=DEBUG)