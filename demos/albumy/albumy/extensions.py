#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   extensions.py
@Time    :   2024/07/26 14:51:11
@Author  :   Alan
@Desc    :   None
'''
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap4 as Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_avatars import Avatars
from flask_whooshee import Whooshee
from flask_debugtoolbar import DebugToolbarExtension


db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
csrf = CSRFProtect()
avatars = Avatars()
whooshee = Whooshee()
debug_toolbar = DebugToolbarExtension()


@login_manager.user_loader
def load_user(user_id):
  from albumy.models import User
  return User.query.get(int(user_id))