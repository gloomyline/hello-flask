#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   models.py
@Time    :   2024/07/23 13:50:41
@Author  :   Alan
@Desc    :   None
'''
from datetime import datetime, UTC
from noteboard import db

class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(200))
  name = db.Column(db.String(20))
  timestamp = db.Column(db.DateTime, default=datetime.now(UTC), index=True)
