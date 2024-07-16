# -*- coding: utf-8 -*-

import os

from flask import Flask
from todoism.settings import config
from todoism.extensions import register_extensions
from todoism.bps import register_blueprints
from todoism.commands import register_commands
from todoism.errors import register_errors


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
