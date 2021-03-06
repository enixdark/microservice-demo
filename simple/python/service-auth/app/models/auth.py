from app import db
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_validator import (ValidateString, ValidateEmail, ValidateBoolean)
from .base import CRUDMixin

class Auth(CRUDMixin, db.Model):
    __tablename__ = 'auths'
    id = db.Column(db.String,primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String())
    token = db.Column(db.String())
    is_delete = db.Column(db.Boolean, unique=False, default=False)
    def __init__(self, id, email, password, token="", is_delete=False):
        self.id = id
        self.setpassword(password)
        self.email = email
        self.is_delete = is_delete
        self.token = token
    
    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def setpassword(self, password):
        self.password = generate_password_hash(password)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            if(attr == 'password'):
                self.setpassword(value)
            elif value != None:
                setattr(self, attr, value)
        return self.save() or self

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def __declare_last__(cls):
        ValidateString(Auth.password)
        ValidateEmail(Auth.email)
        ValidateBoolean(Auth.is_delete)

    def __repr__(self):
        return '<Auth %s>' % self.email
