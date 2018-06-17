from app import db
from werkzeug.security import (generate_password_hash, check_password_hash)
from flask_validator import (ValidateString, ValidateEmail, ValidateBoolean)
from .base import CRUDMixin
import enum

class UserRole(enum.Enum):
    MEMBER = "MEMBER"
    MANAGER = "MANAGER"

class User(CRUDMixin, db.Model):
    __tablename__ = 'users'
    # id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    is_active = db.Column(db.Boolean, unique=False, default=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.MEMBER)
    auth_id = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, role, auth_id="", is_active=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = is_active
        self.role = self.role
        self.auth_id = auth_id

    @property
    def full_name(self):
      return f'{self.first_name} {self.last_name}' 

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
        return check_password_hash(self._password, password)

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def __declare_last__(cls):
        ValidateString(User.first_name)
        ValidateString(User.last_name)
        ValidateEmail(User.email)
        ValidateBoolean(User.delete)

    def __repr__(self):
        return '<User %s>' % self.email
