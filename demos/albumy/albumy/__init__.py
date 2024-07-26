#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/07/26 14:26:22
@Author  :   Alan
@Desc    :   None
'''
import os
from flask import Flask

from albumy.settings import config
from albumy.extensions import db, login_manager, bootstrap, moment, \
  mail, csrf, avatars, whooshee, debug_toolbar


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('FLASK_CONFIG', 'development')

  app = Flask('albumy')

  app.config.from_object(config[config_name])

  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errorhandlers(app)
  register_shell_context(app)
  register_template_context(app)


def register_extensions(app):
  db.init(app)
  login_manager.init_app(app)
  bootstrap.init_app(app)
  moment.init_app(app)
  mail.init_app(app)
  csrf.init_app(app)
  avatars.init_app(app)
  whooshee.init_app(app)
  debug_toolbar.init_app(app)


def register_blueprints(app):
  pass


def register_commands(app):
  pass


def register_errorhandlers(app):
  pass


def register_shell_context(app):
  pass


def register_template_context(app):
  pass