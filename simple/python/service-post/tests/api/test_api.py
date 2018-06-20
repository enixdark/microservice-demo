import unittest
# from faker import Faker
from app import application, db
from app.models.post import Post
import json
import datetime
from bson.objectid import ObjectId


class TestApi(unittest.TestCase):

    def setUp(self):
        # application.config.from_pyfile('config/test.cfg')
        application.config['TESTING'] = True
        self.client = application.test_client()
        self.db = db
        gen_time = datetime.datetime.now()
        dummy_id = ObjectId.from_datetime(gen_time)
        self.post = Post.create(
            id=dummy_id,
            title='chao buoi sang',
            content='day la mini project de demo ve microservice',
            tags=['microservice', 'python', 'docker'],
            account_id='1'
        )

    def tearDown(self):
        db = self.db.connect(application.config)
        db.drop_database(application.config['MONGODB_DB'])

    def test_get_post(self):
        response = self.client.get(
            '/post/%s' % str(self.post.id),
        )
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'chao buoi sang')
        self.assertEqual(data['content'], 'day la mini project de demo ve microservice')

    def test_create_post(self):
        self.assertEqual(Post.objects.count(), 1)
        response = self.client.post(
            '/posts', data=json.dumps({
                'title': 'chao buoi sang',
                'content': 'day la mini project de demo ve microservice',
                'tags': ['microservice', 'python', 'docker'],
                'account_id': '1'
            }), content_type='application/json'
        )
        self.assertEqual('202 ACCEPTED', response.status)
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post(self):
        post = Post.objects.first()
        response = self.client.put(
            '/post/%s' % str(post.id),
            data=json.dumps({'title': 'mini microservice'}),
            content_type='application/json'
        )
        self.assertEqual('202 ACCEPTED', response.status)
        post = Post.objects.first()
        self.assertEqual('mini microservice', post.title)

    def test_delete_post(self):
        id = Post.objects.first().id
        self.client.delete(
            '/post/%s' % str(id)
        )
        self.assertEqual(Post.get(id=id), None)


if __name__ == '__main__':
    unittest.main()
