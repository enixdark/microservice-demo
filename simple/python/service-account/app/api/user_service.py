from flask_restful import (
    Resource,
    marshal,
    marshal_with,
    fields,
    reqparse,
    abort)
from app.models.user import User
from flask import request

user_fields = {
    "id": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "role": fields.String,
    "auth_id": fields.String,
    "email": fields.String,
}


class UserBase(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=False,
                                   help='No first name', location='json')
        self.reqparse.add_argument('last_name', type=str, required=False,
                                   help='No last name', location='json')
        self.reqparse.add_argument('role', type=str, required=False,
                                   help='No last name', location='json')
        self.reqparse.add_argument('auth_id', type=str, required=True,
                                   help='No auth id', location='json')
        self.reqparse.add_argument(
            'email',
            type=str,
            default="",
            required=True,
            location='json')
        super(UserBase, self).__init__()


class UserService(UserBase):

    @marshal_with(user_fields)
    def get(self):
        return User.all(), 200

    def post(self):
        args = self.reqparse.parse_args()
        user = User(**args)
        if(user.save()):
            return 'create %s success' % user.full_name, 202
        return ' %s not found' % user.email, 404


class UserServiceList(UserBase):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('first_name', type=str, required=False,
                                   help='No first name', location='json')
        self.reqparse.add_argument('last_name', type=str, required=False,
                                   help='No last name', location='json')
        self.reqparse.add_argument('role', type=str, required=False,
                                   help='No last name', location='json')
        self.reqparse.add_argument('auth_id', type=str, required=True,
                                   help='No auth id', location='json')
        self.reqparse.add_argument('email', type=str, required=True,
                                   help='No email', location='json')
    def get(self, id):
        user = User.get(id)
        if user and (not user.delete):
            return marshal(User.get(id), user_fields), 201
        return "Not Found", 404

    def delete(self, id):
        user = User.get(id)
        if user and (not user.delete):
            user.remove()
            return "Delete success", 204
        return "Not Found", 404

    def put(self, id):
        args = self.reqparse.parse_args()
        user = User.get(id)
        if user and (not user.delete) and user.update(**args):
            return 'update %s success' % user.email, 202
        return ' %s not found' % user.email, 404
