# -*- coding: utf-8 -*-

from todoism.apis.v1.errors import api_abort

def register_errors(app):
  @app.errorhandler(400)
  def bad_request(e):
    return api_abort(400, message='error')