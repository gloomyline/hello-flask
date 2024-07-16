# -*- coding: utf-8 -*-

import os


class BaseConfig:
  TODOISM_LOCALES = ['en_US', 'zh_Hans_CN']
  TODO_ITEMS_PER_PAGE = 20

  BABEL_DEFAULT_LOCALE = TODOISM_LOCALES[1]

  SECRET_KEY = os.getenv('secret_key', 'a secret thing')

  MONGODB_SETTINGS = [
    {
      'db': 'todoism',
      # 'host': 'localhost',
      # 'port': 27017,
      # 'alias': 'default',
      # 'connect': False,
    }
  ]

class DevelopmentConfig(BaseConfig):
  pass

class ProductionConfig(BaseConfig):
  MONGODB_SETTINGS = [
    {
      'db': os.getenv('DB_NAME', 'todoism'),
      'host': os.getenv('MONGO_HOST', 'localhost'),
      'port': os.getenv('MONGO_PORT', 27017),
      'username': os.getenv('MONGODB_ADMIN_USERNAME', 'todoism'),
      'password': os.getenv('MONGODB_ADMIN_PASSWORD', 'PASSWORD')
    }
  ]
  pass

class TestingConfig(BaseConfig):
  TESTING = True

config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig
}