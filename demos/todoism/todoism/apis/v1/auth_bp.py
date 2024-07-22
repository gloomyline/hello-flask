#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth_bp.py
@Time    :   2024/07/17 09:24:12
@Desc    :   auth api include login,logout,etc.
'''


from faker import Faker
from flask import Blueprint, request, jsonify
from flask_babel import _, lazy_gettext as _l
from flask_login import login_user, logout_user, login_required, current_user

from todoism.apis.v1.errors import api_abort, api_respponse
from todoism.models import User, Todo

auth_bp = Blueprint('auth_api', __name__)
fake = Faker()


@auth_bp.route('/login', methods=['POST'])
def login():
  if current_user.is_authenticated:
    return api_abort(302, message=_l('Current user is already authenticated.'))
  
  data = request.get_json()
  username = data['username']
  password = data['password']
  user = User.objects(username=username).first()

  if user is not None and user.validate_password(password):
    login_user(user)
    return api_respponse(code=1, message=_l('Login success.'))
  return jsonify(message=_('Invalid username or password.')), 400

@login_required
@auth_bp.route('/logout')
def logout():
  logout_user()
  return jsonify(message=_('Logout success.'))

@auth_bp.route('/register')
def register():
  # generate a random account
  username = fake.user_name()
  while User.objects(username=username).first() is not None:
    username = fake.user_name()
  password = fake.word()
  user = User(username=username)
  user.set_password(password)
  user.save()

  todo_bodies = [
    'Witness something truly majestic.',
    'Help a complete stranger.',
    'Drive a motorcycle on the Great Wall of China',
    'Sit on the Great Egyptian Pyramids',
  ]
  for x in range(4):
    todo = Todo(body=_(todo_bodies[x]), done=(False, True)[x == 2], author=user)
    todo.save()
  
  return api_respponse(code=1, message=_('Register success.'), data=dict(username=username, password=password))