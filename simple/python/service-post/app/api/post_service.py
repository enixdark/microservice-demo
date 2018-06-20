from flask_restful import (
    Resource,
    reqparse,
)
from app.models.post import Post
from marshmallow_mongoengine import ModelSchema


class PostSchema(ModelSchema):
    class Meta:
        model = Post


post_schema = PostSchema()


class PostBase(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No title', location='json')
        self.reqparse.add_argument(
            'content',
            type=str,
            default="",
            required=False,
            location='json')

        self.reqparse.add_argument(
            'account_id',
            type=str,
            default="",
            required=False,
            location='json')

        self.reqparse.add_argument('tags', type=str, action='append', location='json')
        super(PostBase, self).__init__()


class PostService(PostBase):

    def get(self):
        data, _ = post_schema.dump(Post.all(), many=True)
        return data, 200

    def post(self):
        args = self.reqparse.parse_args()
        post = Post(**args)
        if(post.save()):
            return {'message': 'create post with title %s success' % post.title}, 202
        return {'message': '%s not found' % post.title}, 404


class PostServiceList(PostBase):

    def get(self, id):
        post = Post.get(id=id)
        if post:
            data, _ = post_schema.dump(post)
            return data, 201
        return {'message': 'Not Found'}, 404

    def delete(self, id):
        post = Post.get(id=id)
        if post:
            post.remove()
            return {'message': 'Delete success'}, 204
        return {'message': 'Not Found'}, 404

    def put(self, id):
        args = self.reqparse.parse_args()
        post = Post.get(id=id)
        if post and post.update(**args):
            return {'message': 'update %s success' % post.title}, 202
        return {'message': '%s not found' % post.title}, 404
