# -*- coding: utf-8 -*-

from flask import jsonify, request
from flask.views import MethodView
from todoism.apis.v1.errors import ValidationError, api_abort


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

class AuthTokenApi(MethodView):

  def post(self):
    grant_type = request.form.get('grant_type')
    username = request.form.get('username')
    password = request.form.get('password')

    if grant_type is None or grant_type.lower() != 'password':
      return api_abort(code=400, message='The grant type must be password.')
