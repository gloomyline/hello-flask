# -*- coding: utf-8 -*-

from flask_babel import lazy_gettext as _l
from todoism.apis.v1.errors import api_abort

def register_errors(app):
  @app.errorhandler(400)
  def bad_request(e):
    return api_abort(400, message=_l('Bad Request'))
  
  @app.errorhandler(403)
  def forbidden(e):
    return api_abort(403, message=_l("Forbidden"))
  
  @app.errorhandler(404)
  def not_found(e):
    return api_abort(404, message=_l('The requested URL was not found on the server.'))

  @app.errorhandler(405)
  def method_not_allowed(e):
    return api_abort(405, message=_l('The method is not allowed for the requested URL.'))

  @app.errorhandler(500)
  def internal_server_error(e):
    return api_abort(500, message=_l('An internal server error occurred.'))
