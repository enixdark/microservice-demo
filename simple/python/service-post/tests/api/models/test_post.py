import unittest
# from faker import Faker
from app import application, db
from app.models.post import Post
import datetime
from bson.objectid import ObjectId
from datetime import timedelta


class TestPost(unittest.TestCase):

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

    def test_create_post(self):
        self.assertEqual(Post.objects.count(), 1)
        # add 1 second to avoid the time doesn't change when process run too fast
        gen_time = datetime.datetime.now() + timedelta(seconds=1)
        dummy_id = ObjectId.from_datetime(gen_time)
        self.post = Post.create(
            id=dummy_id,
            title='testing in microservice',
            content='day la bai ve tdd',
            tags=['microservice', 'python', 'docker'],
            account_id='1'
        )
        self.assertEqual(Post.objects.count(), 2)

    def test_get_post(self):
        post = Post.objects.first()
        self.assertEqual("chao buoi sang", post.title)
        self.assertEqual("day la mini project de demo ve microservice", post.content)

    def test_delete_user(self):
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        post.remove()
        self.assertEqual(Post.objects.count(), 0)


if __name__ == '__main__':
    unittest.main()
