# -*- coding: utf-8 -*-

from flask import current_app, g, jsonify, request
from flask.views import MethodView
from flask_babel import lazy_gettext as _l
from todoism.models import User, Todo
from todoism.apis.v1 import api_v1
from todoism.apis.v1.errors import ValidationError, api_abort
from todoism.apis.v1.auth import generate_token, auth_required
from todoism.apis.v1.schemas import todos_schema, user_schema, todo_schema


def get_todo_body():
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
    grant_type = request.json.get('grant_type')
    username = request.json.get('username')
    password = request.json.get('password')

    if grant_type is None or grant_type.lower() != 'password':
      return api_abort(code=400, message='The grant type must be password.')
    
    user = User.objects.get_or_404(username=username)
    if user is None or not user.validate_password(password):
      return api_abort(code=400, message='Either the username or password was invalid.')

    token, expiration = generate_token(user)

    response = jsonify({
      'access_token': token,
      'tokey_type': 'Bearer',
      'expires_in': expiration,
    })
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


class TodoApi(MethodView):
  decorators = [auth_required]

  def get(self, todo_id):
    """Get todo"""
    todo = Todo.objects.get_or_404(id=todo_id)
    if g.current_user != todo.user:
      return api_abort(403)
    return jsonify(todo_schema(todo))

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

  def put(self, todo_id):
    """Edit todo"""
    todo = Todo.objects.get_or_404(id=todo_id)
    if g.current_user != todo.author:
      return api_abort(403)
    Todo.objects(id=todo_id).update(set__body=get_todo_body())
    return '', 204

  def patch(self, todo_id):
    """Toggle todo"""
    todo = Todo.objects.get_or_404(id=todo_id)
    if g.current_user != todo.author:
      return api_abort(403)
    todo.done = not todo.done
    todo.save()
    return '', 204
  
  def delete(self, todo_id):
    """Delete todo"""
    todo = Todo.objects.get_or_404(id=todo_id)
    if g.current_user != todo.author:
      return api_abort(403)
    todo.delete()
    return '', 204


class UserApi(MethodView):
  decorators = [auth_required]

  def get(self):
    return jsonify(user_schema(g.current_user))  
    

class TodosApi(MethodView):
  decorators = [auth_required]

  def get(self):
    """Get current user's all todos"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['TODOISM_ITEM_PER_PAGE']
    pagination = Todo.objects(author=g.current_user).paginate(page, per_page)
    todos = pagination.items
    current = page
    return jsonify(todos_schema(todos, current, pagination))


api_v1.add_url_rule('', view_func=IndexApi.as_view('index'), methods=['GET'])
api_v1.add_url_rule('/oauth/token', view_func=AuthTokenApi.as_view('token'), methods=['POST'])
api_v1.add_url_rule('/user', view_func=UserApi.as_view('user'), methods=['POST','GET'])
api_v1.add_url_rule('/todo', view_func=TodoApi.as_view('todo'), methods=['POST','GET'])
api_v1.add_url_rule('/user/todos', view_func=TodosApi.as_view('todos'), methods=['POST','GET'])