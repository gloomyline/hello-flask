#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   auth.py
@Time    :   2024/07/29 11:19:59
@Author  :   Alan
@Desc    :   auth_bp
'''
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import confirm_login, current_user, login_fresh, login_required, login_user, logout_user

from albumy.settings import Operations
from albumy.extensions import db
from albumy.models import User
from albumy.forms.auth import ForgetPasswordForm, LoginForm, RegisterForm, ResetPasswordForm
from albumy.utils import generate_token, redirect_back, validate_token, clear_cache
from albumy.emails import send_confirm_email, send_reset_password_email


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None and user.validate_password(form.password.data):
      if login_user(user, form.remember_me.data):
        flash('Login success.', 'info')
        clear_cache([f'view/{url_for('main.index')}'])
        return redirect_back()
      else:
        flash('Your account is blocked.', 'warning')
        return redirect(url_for('main.index'))
    flash('Invalid email or password.', 'warning')
  return render_template('auth/login.html', form=form)


@auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
@login_required
def re_authenticate():
  if login_fresh():
    return redirect(url_for('main.index'))

  form = LoginForm()
  if form.validate_on_submit() and current_user.validate_password(form.password.data):
    confirm_login()
    return redirect_back()
  return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Logout success.', 'info')
  return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = RegisterForm()
  if form.validate_on_submit():
    name = form.name.data
    email = form.email.data.lower()
    username = form.username.data
    password = form.password.data
    user = User(name=name, email=email, username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    token = generate_token(user=user, operation=Operations.CONFIRM)
    send_confirm_email(user=user, token=token)
    flash('Confirm email sent, check your inbox.', 'info')
    return redirect(url_for('.login'))
  return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
@login_required
def confirm(token):
  if current_user.confirmed:
    return redirect(url_for('main.index'))

  if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
    flash('Account confirmed.', 'success')
    return redirect(url_for('main.index'))
  else:
    flash('Invalid or expired token.', 'danger')
    return redirect(url_for('.resend_confirm_email'))


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
  if current_user.confirmed:
    return redirect(url_for('main.index'))

  token = generate_token(user=current_user, operation=Operations.CONFIRM)
  send_confirm_email(user=current_user, token=token)
  flash('New email sent, check your inbox', 'info')
  return redirect(url_for('main.index'))


@auth_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = ForgetPasswordForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None:
      token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
      send_reset_password_email(user=user, token=token)
      flash('Password reset email sent, check you inbox.', 'info')
      return redirect(url_for('.login'))
    flash('Invalid email', 'warning')
    return redirect(url_for('.forget_password'))
  return render_template('auth/forget_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))

  form = ResetPasswordForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is None:
      return redirect(url_for('main.index'))
    if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD,
                      new_password=form.password.data):
      flash('Password updated.', 'success') 
      return redirect(url_for('.login'))
    else:
      flash('Invalid or expired link.', 'danger')
      return redirect(url_for('.forget_password'))
  return render_template('auth/reset_password.html', form=form)