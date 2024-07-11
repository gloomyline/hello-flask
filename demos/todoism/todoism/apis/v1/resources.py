# -*- coding: utf-8 -*-

from flask import g, jsonify, request
from flask.views import MethodView
from flask_babel import lazy_gettext as _l
from todoism.models import User, Todo
from todoism.apis.v1 import api_v1
from todoism.apis.v1.errors import ValidationError, api_abort
from todoism.apis.v1.auth import generate_token


def get_item_body():
  data = request.get_json()
  body = data.get('body')
  if body is None or str(body).strip() == '':
    raise ValidationError('The item body was empty or invalid.')
  return body

class IndexApi(MethodView):

  def get(self):
    return jsonify({
      'api_version': '1.0',
      'api_base_url': 'todoism.com/api/v1',
      'current_user_url': 'todoism.com/api/v1/user',
      'authentication_url': 'todoism.com/api/v1/token',
      'item_url': 'todoism.com/api/v1/items/{item_id}',
      'current_user_items_url': 'todoism.com/api/v1/user/items{?page,per_page}',
      'current_user_active_items_url': 'todoism.com/api/v1/user/items/active{?page,per_page}',
      'current_user_completed_items_url': 'todoism.com/api/v1/user/items/completed{?page,per_page}',
    })


class UserApi(MethodView):

  def get(self):
    return jsonify({
      'code': 1,
      'data': g.current_user,
      'message': _l('ok'),
    })
  
  def post(self):
    username = request.json.get('username', 'Human')
    password = request.json.get('password', '123456')
    user = User(username=username)
    user.set_password(password)
    user.save()
    return jsonify({
      'code': 1,
      'data': {
        'username': username,
        'password': user['password_hash'],
      },
      'message': _l('ok')
    })


class TodoApi(MethodView):
  
  def post(self):
    body = request.json.get('body')
    done = request.json.get('done', False)
    author = request.json.get('author')
    todo = Todo(body=body, done=done, author=author)
    todo.save()

    return jsonify({
      'code': 1,
      'data': todo,
      'message': _l('ok')
    })


class AuthTokenApi(MethodView):

  def post(self):
    grant_type = request.json.get('grant_type')
    username = request.json.get('username')
    password = request.json.get('password')

    if grant_type is None or grant_type.lower() != 'password':
      return api_abort(code=400, message='The grant type must be password.')
    
    user = User.objects.get_or_404(username=username)
    if user is None or not user.validate_password(password):
      return api_abort(code=400, message='Either the username or password was invalid.')

    token, expiration = generate_token(user)


api_v1.add_url_rule('', view_func=IndexApi.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/user', view_func=UserApi.as_view('user'), methods=['POST','GET'])
api_v1.add_url_rule('/todo', view_func=TodoApi.as_view('todo'), methods=['POST','GET'])