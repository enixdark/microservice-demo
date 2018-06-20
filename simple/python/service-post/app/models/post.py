from app import db
from flask_validator import ValidateString
from .base import CRUDMixin


class Post(CRUDMixin, db.Document):

    title = db.StringField(required=True)
    content = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    account_id = db.StringField()

    meta = {
        'indexes': [
            'title',
            '$title',  # text index
            '#title',  # hashed index
        ]
    }

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() or self

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def __declare_last__(cls):
        ValidateString(Post.title)
        ValidateString(Post.content)

    def __repr__(self):
        return '<Post %s>' % self.title
