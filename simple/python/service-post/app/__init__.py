import os
from flask import Flask, render_template
# from moment import momentjs
from flask_script import Manager, Server
from flask_debugtoolbar import DebugToolbarExtension
from flask_mongoengine import MongoEngine
from flask_restful import Api
from http import HTTPStatus
import requests
import socket


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


EXTERNAL_IP = get_ip_address()
GATEWAY_URI = 'http://127.0.0.1:8001'

# register service to kong api gateway
response = requests.get(f'{GATEWAY_URI}/services/post-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/services', data={
        "name": "post-service",
        "url": f'http://{EXTERNAL_IP}:9002',
    })

response = requests.get(f'{GATEWAY_URI}/apis/post-service')
if not response.status_code == HTTPStatus.OK:
    response = requests.post(f'{GATEWAY_URI}/apis', data={
        "name": "post",
        "hosts": "127.0.0.1",
        "uris": "/post-service",
        "upstream_url": f'http://{EXTERNAL_IP}:9002',
    })

# set file extension for upload
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

application = Flask(__name__)
application.config.from_pyfile('config/development.cfg')

# register for migrating
db = MongoEngine(application)

from app.api.post_service import PostService, PostServiceList

# register for debugging
toolbar = DebugToolbarExtension(application)

# register script command
manager = Manager(application)
manager.add_command("runserver", Server(host="0.0.0.0", port=9002))

# wrap to api
api = Api(application)
api.add_resource(PostService, '/posts')
api.add_resource(PostServiceList, '/post/<id>')


# app.register_blueprint(api)
