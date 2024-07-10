# -*- coding: utf-8 -*-

import os


class BaseConfig:
  TODOISM_LOCALES = ['en_US', 'zh_Hans_CN']
  TODO_ITEMS_PER_PAGE = 20

  BABEL_DEFAULT_LOCALE = TODOISM_LOCALES[0]

  SECRET_KEY = os.getenv('secret_key', 'a secret thing')

  MONGODB_SETTINGS = [
    {
      'db': 'todoism',
      'host': 'localhost',
      'port': 27017,
      'alias': 'default',
    }
  ]

class DevelopmenConfig(BaseConfig):
  pass

class ProductionConfig(BaseConfig):
  pass

class TestingConfig(BaseConfig):
  TESTING = True

config = {
  'development': DevelopmenConfig,
  'production': ProductionConfig,
  'testing': TestingConfig
}