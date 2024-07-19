#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   home.py
@Time    :   2024/07/19 09:31:21
@Author  :   Alan
@Desc    :   None
'''

from flask import Blueprint, current_app, jsonify, make_response 
from flask_cors import CORS
from flask_babel import lazy_gettext as _l
from flask_login import current_user

from todoism.models import User
from todoism.apis.v1.errors import api_abort


home_bp = Blueprint('home', __name__)
CORS(home_bp)

@home_bp.route('/set-locale/<locale>', methods=['GET', 'POST'])
def set_locale(locale):
  if locale not in current_app.config['TODOISM_LOCALES']:
    return api_abort(code=404, message=_l('Invalid locale.'))
  
  response = make_response(jsonify(code=1, message=_l('Setting updated.')))

  if current_user.is_authenticated:
    current_user.locale = locale
    current_user.save()
  else:
    response.set_cookie('locale', locale, max_age=60*60*24*30)
  
  return response