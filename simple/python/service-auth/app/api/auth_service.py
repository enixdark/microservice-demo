from flask_restful import (
    Resource,
    marshal,
    marshal_with,
    fields,
    reqparse,
    abort)
from app.models.auth import Auth
from flask import request
from .api_service import ApiService

auth_fields = {
    "id": fields.String,
    "password": fields.String,
    "email": fields.String,
    "is_delete": fields.Boolean,
    "token": fields.String,
}

account_info_field = {
    "id": fields.String,
    "email": fields.String,
    "token": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "role": fields.String
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
        self.reqparse.add_argument('token', type=str, location='json')
        self.reqparse.add_argument('is_delete', type=bool, location='json')
        super(AuthBase, self).__init__()

class SignUpService(AuthBase):
    base_url = 'http://127.0.0.1:8001'
    account_service = 'http://127.0.0.1:8000/account-service' 
    
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
        self.reqparse.add_argument('first_name', type=str, required=False,
                                   help='No first name', location='json')
        self.reqparse.add_argument('last_name', type=str, required=False,
                                   help='No last name', location='json')
        self.reqparse.add_argument('role', type=str, required=False,
                                   help='No last name', location='json')
        self.api_gateway = ApiService(base_url=self.base_url)
        self.account_api = ApiService(base_url=self.account_service)
    
    def post(self):
        args = self.reqparse.parse_args()
        auth = Auth.query.filter_by(email=args.get('email')).first()
        if auth:
            return 'the %s already exists' % auth.email, 404
        data = self.api_gateway.post(f'/consumers', data={
            'username': args.get('email'),
        })
        auth = Auth.create(id=data.get('id'), email=args.get('email'), password=args.get('password'))

        response = self.account_api.post(f'/account-service/users', data=dict(args,**{'auth_id': auth.id}))
        return {
            "id": data.get('id'),
            "email": args.get('email'),
            "token": args.get('token'),
            "first_name": args.get('first_name'),
            "last_name": args.get('last_name'),
            "role": args.get('role')
        }

class AuthService(AuthBase):
    base_url = 'http://127.0.0.1:8001'

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
        self.api_gateway = ApiService(base_url=self.base_url)
        super(AuthBase, self).__init__()
        
    
    def post(self):
        args = self.reqparse.parse_args()
        auth = Auth.query.filter_by(email=args.get('email')).first()
        if auth and auth.check_password(args.get('password')):
            response = self.api_gateway.post(f'/consumers/{auth.id}/key-auth', data={})
            return response
        return ' %s not found' % auth.email, 404

class AuthServiceList(AuthBase):

    def get(self, id):
        auth = Auth.get(id)
        if auth and (not auth.is_delete):
            return marshal(auth, auth_fields), 201
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
