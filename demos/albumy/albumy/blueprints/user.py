#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/01 11:36:14
@Author  :   Alan
@Desc    :   bp user
'''
from flask import Blueprint, current_app, flash, render_template, request
from flask_login import current_user, logout_user

from albumy.models import Photo, User


user_bp = Blueprint('user', __name__)

@user_bp.route('/<username>')
def index(username):
  user = User.query.filter_by(username=username).first_or_404()
  if user == current_user and user.locked:
    flash('Your account is locked.', 'danger')
  if user == current_user and not user.active:
    logout_user()

  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
  pagination = Photo.query.with_parent(user) \
                .order_by(Photo.timestamp.desc()).paginate(page=page, per_page=per_page)
  photos = pagination.items
  return render_template('user/index.html', user=user, pagination=pagination, photos=photos)