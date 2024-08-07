#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   decorators.py
@Time    :   2024/07/31 16:57:50
@Author  :   Alan
@Desc    :   None
'''
from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user
from markupsafe import Markup


def confirm_required(func):
  @wraps(func)
  def decorated_func(*args, **kwargs):
    if not current_user.confirmed:
      message = Markup(
        'Please confirm your account first.'
        'Not receive the email?'
        '<a class="alert-link" href="%s"></a>' %
        url_for('auth.resend_confirm_email')
      )
      flash(message, 'warning')
      return redirect(url_for('main.index'))
    return func(*args, **kwargs)
  return decorated_func


def permission_required(permission_name):
  def decorator(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
      if not current_user.can(permission_name):
        abort(401)
      return func(*args, **kwargs)
    return decorated_func
  return decorator


def admin_required(func):
  return permission_required('ADMINISTRATOR')(func)