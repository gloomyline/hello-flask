#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   settings.py
@Time    :   2024/07/24 09:05:08
@Author  :   Alan
@Desc    :   None
'''

import os
import sys


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN is not None:
  prefix = 'sqlite:///'
else:
  prefix = 'sqliete:////'

class BaseConfig():
  SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

  DEBUG_TB_INTECEPT_REDIRECTS = False

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = False

  CKEDITOR_ENABLE_CSRF = True
  CKEDITOR_FILE_UPLOADER = 'admin.upload_image'
  
  MAIL_SERVER = os.getenv('MAIL_SERVER')
  MAIL_PORT = 465
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
  MAIL_DEFAULT_SENDER = ('Blog Admin', MAIL_USERNAME)
  
  BLOG_EMAIL = os.getenv('BLOG_EMAIL')
  BLOG_POST_PER_PAGE = 10
  BLOG_MANAGE_POST_PER_PAGE = 20
  BLOG_COMMENT_PER_PAGE = 20
  BLOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
  BLOG_SLOW_QUERY_THRESHOLD = 1

  BLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
  BLOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'svg']


class DevelopmentConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
  TESTING = True
  WTF_CSRF_ENABLED = False
  SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # in-memory database
  

class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}