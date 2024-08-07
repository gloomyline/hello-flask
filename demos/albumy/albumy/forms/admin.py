#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   admin.py
@Time    :   2024/08/07 09:35:49
@Author  :   Alan
@Desc    :   Admin Form
'''
from wtforms import StringField, SelectField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email

from albumy.models import Role, User
from albumy.forms.user import EditProfileForm


class EditProfileAdminForm(EditProfileForm):
  email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
  role = SelectField('Role', coerce=int)
  active = BooleanField('Active')
  confirmed = BooleanField('Confirmed')
  submit = SubmitField()

  def __init__(self, user, *args, **kwargs):
    super(EditProfileAdminForm, self).__init__(*args, **kwargs)
    self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
    self.user = user


  # def validate_username(self, field):
  #   if field.data != self.user.username and User.query.filter_by(username=field.data).first():
  #     return ValidationError('The username already exists')


  def validate_email(self, field):
    if field.data != self.user.email and User.query.filter_by(email=field.data.lower()).first():
      return ValidationError('The email already exists')
