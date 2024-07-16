
from todoism.apis.v1 import api_v1


def register_blueprints(app):
  # enable subdomain support
  # app.register_blueprint(api_v1, url_prefix='/v1', subdomain = 'api') 
  app.register_blueprint(api_v1, url_prefix='/api/v1')