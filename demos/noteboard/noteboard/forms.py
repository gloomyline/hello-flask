#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   forms.py
@Time    :   2024/07/23 13:54:39
@Author  :   Alan
@Desc    :   None
'''

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class BoardForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
  body = TextAreaField('Body', validators=[DataRequired(), Length(1, 200)])
  submit = SubmitField()