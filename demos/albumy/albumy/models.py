#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2024/07/26 14:54:31
@Author  :   Alan
@Desc    :   None
'''
from albumy.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)