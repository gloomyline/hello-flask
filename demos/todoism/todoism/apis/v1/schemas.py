from flask import url_for

from todoism.models import Todo

def user_schema(user):
  return {
    'id': user.id,
    'kind': 'User',
    'username': user.username,
    'all_todo_count': len(Todo.objects.all()),
  }