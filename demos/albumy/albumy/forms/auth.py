#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/07/29 10:53:58
@Author  :   Alan
@Desc    :   None
'''
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from albumy.models import User


class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Length(1, 20)])
  password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
  remember_me = BooleanField('Remember me')
  submit = SubmitField()


class RegisterForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
  email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
  username = StringField('Username', validators=[
      DataRequired(), Length(1, 20),
      Regexp('^[a-zA-Z0-9.]*$', message='The username should only contain alphanumeric and dot.')
    ]
  )
  password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
  password2 = PasswordField('Confirm password', validators=[DataRequired()])
  submit = SubmitField()

  def validate_email(self, field):
    if User.query.filter_by(email=field.data.lower()).first():
      raise ValidationError('The email is already in use.')

  def validate_username(self, field):
    if User.query.filter_by(username=field.data).first():
      raise ValidationError('The username is already in use.')


class ForgetPasswordForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
  sumbmit = SubmitField()


class ResetPasswordForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
  password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
  password2 = PasswordField('Password confirm', validators=[DataRequired()])
  submit = SubmitField()