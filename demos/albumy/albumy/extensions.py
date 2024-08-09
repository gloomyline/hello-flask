#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   extensions.py
@Time    :   2024/07/26 14:51:11
@Author  :   Alan
@Desc    :   None
'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_bootstrap import Bootstrap4 as Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_avatars import Avatars
from flask_whooshee import Whooshee
from flask_dropzone import Dropzone
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension


db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
csrf = CSRFProtect()
avatars = Avatars()
whooshee = Whooshee()
dropzone = Dropzone()
migrate = Migrate()
debug_toolbar = DebugToolbarExtension()


@login_manager.user_loader
def load_user(user_id):
  from albumy.models import User
  return User.query.get(int(user_id))

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = 'Please go to confirm'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):
  def can(self, permission_name):
    return False

  @property
  def is_admin(self): 
    return False

login_manager.anonymous_user = Guest