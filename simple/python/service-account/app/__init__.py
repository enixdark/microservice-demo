import os
from flask import Flask, render_template
# from moment import momentjs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from http import HTTPStatus
import requests
import json
import socket




def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

EXTERNAL_IP = get_ip_address()
GATEWAY_URI = 'http://127.0.0.1:8001'


response = requests.get(f'{GATEWAY_URI}/services/account-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/services', data={
        "name": "account-service",
        "url": f'http://{EXTERNAL_IP}:9001',
        # "path": "/account",
    })
response = requests.get(f'{GATEWAY_URI}/apis/account-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/apis', data={
        "name": "account",
        "hosts": "127.0.0.1",
        "uris": "/account-service",
        "upstream_url": f'http://{EXTERNAL_IP}:9001',
    })


# set file extension for upload
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



application = Flask(__name__)

# , instance_path=os.path.join( os.path.dirname(os.path.dirname(__file__)),
#   'app/config'),instance_relative_config=True

# app.jinja_env.globals['momentjs'] = momentjs


application.config.from_pyfile('config/development.cfg')

#
db = SQLAlchemy(application)


# register for migrating
# db = MongoEngine(app)
migrate = Migrate(application, db)


from app.api.user_service import UserService, UserServiceList


# register for debugging
toolbar = DebugToolbarExtension(application)

# register script command
manager = Manager(application)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=9001))

# wrap to api
api = Api(application)
api.add_resource(UserService, '/users')
api.add_resource(UserServiceList, '/user/<id>')


# app.register_blueprint(api)
