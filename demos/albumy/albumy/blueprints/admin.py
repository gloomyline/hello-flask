#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   admin.py
@Time    :   2024/08/06 15:57:45
@Author  :   Alan
@Desc    :   None
'''
from flask import Blueprint, render_template, flash, request, current_app
from flask_login import login_required

from albumy.models import User, Photo, Tag, Comment
from albumy.decorators import admin_required, permission_required
from albumy.models import Role
from albumy.extensions import db
from albumy.forms.admin import EditProfileAdminForm
from albumy.utils import redirect_back


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
@login_required
@permission_required('MODERATE')
def index():
  user_count = User.query.count()
  locked_user_count = User.query.filter_by(locked=True).count()
  blocked_user_count = User.query.filter_by(active=False).count()
  photo_count = Photo.query.count()
  reported_photos_count = Photo.query.filter(Photo.flag > 0).count()
  tag_count = Tag.query.count()
  comment_count = Comment.query.count()
  reported_comments_count = Comment.query.filter(Comment.flag > 0).count()
  return render_template('admin/index.html',
                         user_count=user_count,
                         locked_user_count=locked_user_count,
                         blocked_user_count=blocked_user_count,
                         photo_count=photo_count,
                         reported_photos_count=reported_photos_count,
                         tag_count=tag_count,
                         comment_count=comment_count,
                         reported_comments_count=reported_comments_count)


@admin_bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(user_id):
  user = User.query.get_or_404(user_id)
  form = EditProfileAdminForm(user=user)
  if form.validate_on_submit():
    user.name = form.name.data
    role = Role.query.get(form.role.data)
    if role.name == 'Locked':
      user.lock()
    user.role = role
    user.bio = form.bio.data
    user.website = form.website.data
    user.confirmed = form.confirmed.data
    user.active = form.active.data
    user.location = form.location.data
    user.username = form.username.data
    user.email = form.email.data
    db.session.commit()
    flash('Profile updated.', 'success')
    return redirect_back()
  form.name.data = user.name
  form.role.data = user.role
  form.bio.data = user.bio
  form.website.data = user.website
  form.confirmed.data = user.confirmed
  form.active.data = user.active
  form.location.data = user.location
  form.username.data = user.username
  form.email.data = user.email
  return render_template('admin/edit_profile_admin.html', form=form, user=user)


@admin_bp.route('/block/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def block_user(user_id):
  user = User.query.get_or_404(user_id)
  if user.role.name in ['Administrator', 'Moderator']:
    flash('Permiss denied.', 'warning')
  else:
    user.block()
    flash('Account blocked.', 'info')
  return redirect_back()


@admin_bp.route('/unblock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def unblock_user(user_id):
  user = User.query.get_or_404(user_id)
  user.unblock()
  flash('Account unblocked.', 'info')
  return redirect_back()


@admin_bp.route('/lock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def lock_user(user_id):
  user = User.query.get_or_404(user_id)
  if user.role.name in ['Administrator', 'Moderator']:
    flash('Permission denied.', 'warning')
  else:
    user.lock()
    flash('Account locked.', 'info')
  return redirect_back()


@admin_bp.route('/unlock/user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('MODERATE')
def unlock_user(user_id):
  user = User.query.get_or_404(user_id)
  user.unlock()
  flash('Account unlocked.', 'info')
  return redirect_back()


@login_required
@permission_required('MODERATE')
@admin_bp.route('/delete/tag/<int:tag_id>', methods=['GET', 'POST'])
def delete_tag(tag_id):
  tag = Tag.query.get_or_404(tag_id)
  db.session.delete(tag)
  db.session.commit()
  flash('Tag deleted.', 'info')
  return redirect_back()


@admin_bp.route('/manage/user')
@login_required
@permission_required('MODERATE')
def manage_user():
  # 'all', 'locked', 'blocked', 'administrator', 'moderator'
  filter_rule = request.args.get('filter', 'all')
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_MANAGE_USER_PER_PAGE']
  administrator = Role.query.filter_by(name='Administrator').first()
  moderator = Role.query.filter_by(name='Moderator').first()
  if filter_rule == 'locked':
    filter_users = User.query.filter_by(locked=True)
  elif filter_rule == 'blocked': 
    filter_users = User.query.filter_by(active=False)
  elif filter_rule == 'administrator':
    filter_users = User.query.with_parent(administrator)
  elif filter_rule == 'moderator':
    filter_users = User.query.with_parent(moderator)
  else:
    filter_users = User.query

  pagination = filter_users.order_by(User.member_since.desc()) \
                          .paginate(page=page, per_page=per_page)
  users = pagination.items
  return render_template('admin/manage_user.html', users=enumerate(users), pagination=pagination)


@admin_bp.route('/manage/photo', defaults={'order': 'by_flag'})
@admin_bp.route('/manage/photo/<order>')
@login_required
@permission_required('MODERATE')
def manage_photo(order):
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_MANAGE_PHOTO_PER_PAGE']
  order_rule = 'flag'
  if order == 'by_time':
    pagination = Photo.query.order_by(Photo.timestamp.desc()) \
                              .paginate(page=page, per_page=per_page)
    order_rule = 'time'
  else:
    pagination = Photo.query.order_by(Photo.flag.desc()) \
                              .paginate(page=page, per_page=per_page)
  photos = pagination.items
  return render_template('admin/manage_photo.html', photos=enumerate(photos), pagination=pagination, order_rule=order_rule)


@admin_bp.route('/manage/tag', defaults={'order': 'desc'})
@admin_bp.route('/manage/tag/<order>')
@login_required
@permission_required('MODERATE')
def manage_tag(order):
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_MANAGE_TAG_PER_PAGE']
  order_rule = 'desc'
  if order == 'desc':
    pagination = Tag.query.order_by(Tag.id.desc()) \
                            .paginate(page=page, per_page=per_page)
  else:
    pagination = Tag.query.order_by(Tag.id.asc()) \
                            .paginate(page=page, per_page=per_page)
    order_rule = 'asc'
  tags = pagination.items
  return render_template('admin/manage_tag.html', tags=tags, pagination=pagination, order_rule=order_rule)


@admin_bp.route('/manage/comment', defaults={'order': 'by_flag'})
@admin_bp.route('/manage/comment/<order>')
@login_required
@permission_required('MODERATE')
def manage_comment(order):
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_MANAGE_COMMENT_PER_PAGE']
  order_rule = 'flag'
  if order == 'by_time':
    pagination = Comment.query.order_by(Comment.timestamp.desc()) \
                                .paginate(page=page, per_page=per_page)
    order_rule = 'time'
  else:
    pagination = Comment.query.order_by(Comment.flag.desc()) \
                                .paginate(page=page, per_page=per_page)
  comments = pagination.items
  return render_template('admin/manage_comment.html',
          pagination=pagination, comments=enumerate(comments), order_rule=order_rule)
