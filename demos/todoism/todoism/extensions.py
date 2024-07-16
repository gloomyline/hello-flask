# -*- coding: utf-8 -*-

import os

from flask import current_app, request
from flask_login import LoginManager, current_user as _c_u
from flask_babel import Babel, lazy_gettext as _l
from flask_mongoengine import MongoEngine

db = MongoEngine()
babel = Babel()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = _l('Please login to access the this page.')


@login_manager.user_loader
def load_user(user_id):
  pass

def get_locale():
  if _c_u.is_authenticated and _c_u.locale is not None:
    return _c_u.locale

  locale = request.cookies.get('locale')
  if locale is not None:
    return locale
  
  return request.accept_languages.best_match(current_app.config['TODOISM_LOCALES'])


def register_extensions(app):
  db.init_app(app)
  login_manager.init_app(app)
  babel.init_app(app, locale_selector=get_locale)