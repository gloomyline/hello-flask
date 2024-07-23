# -*- coding: utf-8 -*-

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from todoism.extensions import db
from flask_mongoengine.wtf import fields as mongo_fields
from mongoengine import ReferenceField


class User(db.Document, UserMixin):
  id = db.SequenceField(primary_key=True)
  username = db.StringField(required=True, unique=True)
  password_hash = db.StringField(
    required=True,
    wtf_field_class=mongo_fields.MongoPasswordField,
  )
  locale = db.StringField(max_length=20)

  def __repr__(self):
    return '<User %r>' % self.usernmae

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def validate_password(self, password):
    return check_password_hash(self.password_hash, password)


class Todo(db.Document):
  id = db.SequenceField(primary_key=True)
  body = db.StringField(default='')
  done = db.BooleanField(default=False)
  author = ReferenceField('User', reverse_delete_rule=db.CASCADE)