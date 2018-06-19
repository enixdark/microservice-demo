import os
import unittest
# from faker import Faker
from app import application, db
from app.models.auth import Auth
import tempfile


class TestUser(unittest.TestCase):

    def setUp(self):
        # self.db, application.config['DATABASE'] = tempfile.mkstemp()
        # import ipdb;ipdb.set_trace()

        application.config.from_pyfile('config/test.cfg')
        application.config['TESTING'] = True
        self.client = application.test_client()
        self.db = db
        self.db.create_all()
        self.auth = Auth.create(
            email="cqshinn92@gmail.com",
            password='12345678',
            token='SUmnfqii5wcuJz8WZrWJw66AsE9',
        )

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

    def test_create_auth(self):
        self.assertEqual(Auth.query.count(), 1)
        self.auth = Auth.create(
            password='12345678',
            email='hello@example.com'
        )
        self.assertEqual(Auth.query.count(), 2)

    def test_get_auth(self):
        auth = Auth.query.first()
        self.assertEqual("cqshinn92@gmail.com", auth.email)
        self.assertEqual(False, auth.is_delete)

    def test_delete_auth(self):
        auth = Auth.query.first()
        self.assertEqual(False, auth.is_delete)
        auth.remove()
        self.assertEqual(True, auth.is_delete)

if __name__ == '__main__':
    unittest.main()
