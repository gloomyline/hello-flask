#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   extensions.py
@Time    :   2024/07/24 09:57:43
@Author  :   Alan
@Desc    :   None
'''
from flask_bootstrap import Bootstrap4 as Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_moment import Moment
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()
csrf = CSRFProtect()
migrate = Migrate()
ckeditor = CKEditor()
mail = Mail()
toolbar = DebugToolbarExtension()


@login_manager.user_loader
def load_user(id):
  from blog.models import Admin
  user = Admin.query.get(id)
  return user

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please go to login~'
login_manager.login_message_category = 'warning'