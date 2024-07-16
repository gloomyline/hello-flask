from flask import url_for

from todoism.models import User, Todo

def user_schema(user):
  return {
    'id': user.id,
    'kind': 'User',
    'username': user.username,
    'all_todo_count': len(Todo.objects.find(author=user.id).all()),
  }

def todo_schema(todo):
  return {
    'id': todo.id,
    'kind': 'Todo',
    'body': todo.body,
    'done': todo.done,
    'author': {
      'id': todo.author,
      'username': User.objects.get_or_404(id=todo.author)['username'],
      'kind': 'User',
    }
  }

def todos_schema(todos, current, pagination):
  return {
    'kind': 'TodoCollection',
    'todos': [todo_schema(todo) for todo in todos],
    'current': current,
    'pages': pagination.pages,
    'count': pagination.total
  }