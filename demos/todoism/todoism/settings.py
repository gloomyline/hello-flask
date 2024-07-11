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
      'host': 'localhost',
      'port': 27017,
      'alias': 'default',
    }
  ]

class DevelopmentConfig(BaseConfig):
  pass

class ProductionConfig(BaseConfig):
  pass

class TestingConfig(BaseConfig):
  TESTING = True

config = {
  'development': DevelopmentConfig,
  'production': ProductionConfig,
  'testing': TestingConfig
}