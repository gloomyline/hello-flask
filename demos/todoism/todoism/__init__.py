# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template
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
  app.template_folder = app.root_path + app.config.get('TEMPLATE_FOLDER', '/template')
  # app.static_url_path = app.config.get('STATIC_URL_PATH', '')

  @app.route('/')
  def index():
    return render_template('index.html') 

  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errors(app)
  return app
