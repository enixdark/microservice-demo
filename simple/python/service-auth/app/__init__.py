import os
from flask import Flask, render_template
# from moment import momentjs
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server
from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from http import HTTPStatus
import socket
import requests

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

EXTERNAL_IP = get_ip_address()
GATEWAY_URI = 'http://127.0.0.1:8001'

# register service to kong api gateway
response = requests.get(f'{GATEWAY_URI}/services/auth-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/services', data={
        "name": "auth-service",
        "url": f'http://{EXTERNAL_IP}:9000',
    })

response = requests.get(f'{GATEWAY_URI}/apis/auth-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/apis', data={
        "name": "auth",
        "hosts": "127.0.0.1",
        "uris": "/auth-service",
        "upstream_url": f'http://{EXTERNAL_IP}:9000',
    })

# set file extension for upload
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



application = Flask(__name__)
application.config.from_pyfile('config/development.cfg')

#
db = SQLAlchemy(application)


# register for migrating
# db = MongoEngine(app)
migrate = Migrate(application, db)


from app.api.auth_service import (
    AuthService, 
    AuthServiceList,
    SignUpService,
)


# register for debugging
toolbar = DebugToolbarExtension(application)

# register script command
manager = Manager(application)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server(host="0.0.0.0", port=9000))

# wrap to api
api = Api(application)
api.add_resource(SignUpService, '/register')
api.add_resource(AuthService, '/login')
api.add_resource(AuthServiceList, '/auth/<id>')

# app.register_blueprint(api)
