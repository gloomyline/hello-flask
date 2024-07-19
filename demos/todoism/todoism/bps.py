#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   bps.py
@Time    :   2024/07/18 14:44:30
@Author  :   Alan
@desc    :   register blueprints
'''


from todoism.apis.v1.auth_bp import auth_bp
from todoism.apis.v1.home import home_bp
from todoism.apis.v1 import api_v1


def register_blueprints(app):
  app.register_blueprint(home_bp, url_prefix='/api/v1')
  app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
  # enable subdomain support
  # app.register_blueprint(api_v1, url_prefix='/v1/resources', subdomain = 'api') 
  app.register_blueprint(api_v1, url_prefix='/api/v1/resources')
