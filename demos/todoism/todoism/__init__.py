# -*- coding: utf-8 -*-

import os

from flask import Flask
from todoism.settings import config
from todoism.extensions import db, babel, get_locale, login_manager
from todoism.commands import register_commands
from todoism.errors import register_errors
from todoism.apis.v1 import api_v1


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('flask_config', 'development')

  app = Flask('todoism')
  app.config.from_object(config[config_name])

  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errors(app)
  return app


def register_extensions(app):
  db.init_app(app)
  login_manager.init_app(app)
  babel.init_app(app, locale_selector=get_locale)


def register_blueprints(app):
  # enable subdomain support
  # app.register_blueprint(api_v1, url_prefix='/v1', subdomain = 'api') 
  app.register_blueprint(api_v1, url_prefix='/api/v1')

