#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   forms.py
@Time    :   2024/07/24 15:30:07
@Author  :   Alan
@Desc    :   None
'''
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, SelectField, StringField, SubmitField, TextAreaField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Optional, URL

from blog.models import Category, Link

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
  password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
  remember = BooleanField('Remember me')
  submit = SubmitField('Log in.')


class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired(), Length(1, 30)])
  category = SelectField('Category', coerce=int, default=1)
  body = TextAreaField('Body', validators=[DataRequired()])
  submit = SubmitField()

  def __init__(self, *args, **kwargs):
    super(PostForm, self).__init__(*args, **kwargs)
    self.category.choices = [
      (category.id, category.name) for category in Category.query.order_by(Category.name).all()
    ]


class CategoryForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
  submit = SubmitField()

  def validate_name(self, field):
    if Category.query.filter_by(name=field.data).first():
      raise ValidationError('Name already in use.')


class LinkForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
  url = StringField('Url', validators=[DataRequired(), URL(), Length(1, 255)])
  submit = SubmitField()

  def validate_name(self, field):
    if Link.query.filter_by(name=field.data).first():
      raise ValidationError('Name already in use.')


class CommentForm(FlaskForm):
  author = StringField('Name', validators=[DataRequired(), Length(1, 30)])
  email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254)])
  site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
  body = TextAreaField('Comment', validators=[DataRequired()])
  submit = SubmitField()


class AdminCommentForm(CommentForm):
  author = HiddenField()
  email = HiddenField()
  site = HiddenField()


class SettingsForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
  blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 60)])
  blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 100)])
  about = CKEditorField('Body', validators=[DataRequired()])
  submit = SubmitField()