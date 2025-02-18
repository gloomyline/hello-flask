#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/07/24 16:27:49
@Author  :   Alan
@Desc    :   None
'''
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from blog.forms import LoginForm
from blog.models import Admin
from blog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('essay.index'))

  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    remember = form.remember.data
    admin = Admin.query.first()
    if admin:
      if username == admin.username and admin.validate_password(password):
        login_user(admin, remember)
        flash('Welcome back~', 'info')
        return redirect_back()
      flash('Invalid username or password.', 'warning')
    else:
      flash('No account', 'warning')
  
  return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout success', 'info')
  return redirect_back()