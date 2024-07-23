#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2024/07/23 13:35:45
@Author  :   Alan
@Desc    :   None
'''

import os
import sys

from noteboard import app

# SQLite URI cmpatible
prefix = ''
WIN = sys.platform.startswith('win')
if WIN:
  prefix = 'sqlite:///'
else:
  prefix = 'sqlite:////'

dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret thing')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)