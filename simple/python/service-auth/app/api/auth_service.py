from flask_restful import (
    Resource,
    marshal,
    marshal_with,
    fields,
    reqparse,
    abort)
from app.models.auth import Auth
from flask import request

auth_fields = {
    "id": fields.String,
    "password": fields.String,
    "email": fields.String,
    "is_delete": fields.Boolean
}


class AuthBase(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'password',
            type=str,
            default="",
            required=True,
            location='json'
        )
        self.reqparse.add_argument(
            'email',
            type=str,
            default="",
            required=True,
            location='json'
        )
        self.reqparse.add_argument('delete', type=bool, location='json')
        super(AuthBase, self).__init__()

class AuthService(AuthBase):
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
     
    def post(self):
        args = self.reqparse.parse_args()
        auth = Auth(**args)
        if(auth.save()):
            return 'create %s success' % auth.email, 202
        return ' %s not found' % auth.email, 404

class AuthServiceList(AuthBase):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def get(self, id):
        auth = Auth.get(id)
        if auth and (not auth.is_delete):
            return marshal(Auth.get(id), auth_fields), 201
        return "Not Found"

    def delete(self, id):
        auth = Auth.get(id)
        if auth and (not auth.is_delete):
            auth.remove()
            return "Delete success", 204
        return "Not Found", 404

    def put(self, id):
        args = self.reqparse.parse_args()
        auth = Auth.get(id)
        if auth and (not auth.is_delete) and auth.update(**args):
            return 'update %s success' % auth.email, 202
        return ' %s not found' % auth.email, 404
