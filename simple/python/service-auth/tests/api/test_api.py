import os
import unittest
# from faker import Faker
from app import application, db
from app.models.auth import Auth
import json


class TestApi(unittest.TestCase):

    def setUp(self):
        # self.db, application.config['DATABASE'] = tempfile.mkstemp()
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

    def test_get_user(self):
        response = self.client.get(
            '/auth/%d' % self.auth.id,
        )
        data = json.loads(response.data)
        self.assertEqual(data['email'], "cqshinn92@gmail.com")
        self.assertEqual(data['token'], "SUmnfqii5wcuJz8WZrWJw66AsE9")
        self.assertEqual(data['is_delete'], False)

    def test_sign_in_user(self):
        import pdb;pdb.set_trace()
        self.assertEqual(Auth.query.count(), 1)
        response = self.client.post(
            '/auth', data=json.dumps({
                       "email": "cqshinn92@example.com",
                       "password": "12345678"
                    }), content_type='application/json'
        )
        # self.assertEqual('202 ACCEPTED', response.status)
        # self.assertEqual(User.query.count(), 2)

    def test_update_auth_user(self):
        auth = Auth.query.first()
        response = self.client.put(
            '/auth/%d' % auth.id, data=json.dumps({
                "email": "quancong@gmail.com",
                "password": "12345678"
            }), content_type='application/json'
        )
        self.assertEqual('202 ACCEPTED', response.status)
        auth = Auth.query.first()
        self.assertEqual("quancong@gmail.com", auth.email)

    def test_delete_auth(self):
        id = Auth.query.first().id
        response = self.client.delete(
            '/auth/%d' % self.auth.id
        )
        self.assertEqual(Auth.query.filter_by(id=id).first().is_delete, True)

if __name__ == '__main__':
    unittest.main()
