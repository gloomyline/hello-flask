# -*- coding: utf-8 -*-

import os

from flask import Flask, redirect 
from todoism.settings import config
from todoism.extensions import register_extensions
from todoism.bps import register_blueprints
from todoism.commands import register_commands
from todoism.errors import register_errors


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('flask_config', 'development')

  # config 
  app = Flask('todoism', static_url_path='')
  # app = Flask('todoism')
  app.config.from_object(config[config_name])
  app.template_folder = app.root_path + app.config['TEMPLATE_FOLDER']

  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errors(app)

  @app.route('/')
  def index():
    # static_folder default value is 'static'
    return app.send_static_file('index.html')

  @app.route('/static/')
  def index_static():
    return redirect('/')

  return app
