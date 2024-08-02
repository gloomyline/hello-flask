#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   user.py
@Time    :   2024/08/01 11:36:14
@Author  :   Alan
@Desc    :   bp user
'''
from flask import Blueprint, current_app, flash, render_template, \
                    request, url_for, redirect
from flask_login import current_user, fresh_login_required, login_required, logout_user

from albumy.settings import Operations
from albumy.extensions import db, avatars
from albumy.models import Collect, Photo, User
from albumy.decorators import confirm_required, permission_required
from albumy.notifications import push_follow_notification
from albumy.emails import send_change_email
from albumy.forms.user import ChangeEmailForm, ChangePasswordForm, CropAvatarForm, DeleteAccountForm, \
                        EditProfileForm, NotificationSettingForm, PrivacySettingForm, UploadAvatarForm
from albumy.utils import flash_errors, generate_token, redirect_back, validate_token


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
                .order_by(Photo.timestamp.desc()) \
                .paginate(page=page, per_page=per_page)
  photos = pagination.items
  return render_template('user/index.html',
                         user=user, pagination=pagination, photos=photos)


@user_bp.route('/<username>/collections')
def show_collections(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_PHOTO_PER_PAGE']
  pagination = Collect.query.with_parent(user) \
    .order_by(Collect.timestamp.desc()) \
    .paginate(page=page, per_page=per_page)
  collects = pagination.items
  return render_template('user/collections.html',
                         user=user, pagination=pagination, collects=collects)


@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
@confirm_required
@permission_required('FOLLOW')
def follow(username):
  user = User.query.filter_by(username=username).first_or_404()
  if current_user.is_following(user):
    flash('Already followed.', 'info')
    return redirect(url_for('.index', username=username))

  current_user.follow(user)
  flash('User Followed.', 'info')
  if user != current_user and user.receive_follow_notification:
    push_follow_notification(follower=current_user, receiver=user)
  return redirect_back()


@user_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
  user = User.query.filter_by(username=username).first_or_404()
  if not current_user.is_following(user):
    flash('User has not been followed.', 'warning')
    return redirect(url_for('user.inex', username=username))
  
  current_user.unfollow(user)
  flash('User Unfollowed.', 'info')
  return redirect_back()
  

@user_bp.route('/<username>/followers')
def show_followers(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_USER_PER_PAGE']
  pagination = user.followers.paginate(page=page, per_page=per_page)
  follows = pagination.items
  return render_template('user/followers.html',
                         user=user, follows=follows, pagination=pagination)


@user_bp.route('/<username>/following')
def show_following(username):
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  per_page = current_app.config['ALBUMY_USER_PER_PAGE']
  pagination = user.following.paginate(page=page, per_page=per_page)
  follows = pagination.items
  return render_template('user/following.html',
                         user=user, follows=follows, pagination=pagination)


@user_bp.route('/setting/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.username = form.username.data
    current_user.bio = form.bio.data
    current_user.website = form.website.data
    current_user.location = form.location.data
    db.sesion.commit()
    flash('Profile updated.', 'success')
    return redirect(url_for('.index', username=current_user.username))
  form.name.data = current_user.name
  form.username.data = current_user.username
  form.bio.data = current_user.bio
  form.website.data = current_user.website
  form.location.data = current_user.location
  return render_template('user/settings/edit_profile.html', form=form)


@user_bp.route('/setting/avatar')
@login_required
@confirm_required
def change_avatar():
  upload_form = UploadAvatarForm()
  crop_form = CropAvatarForm()
  return render_template('user/settings/change_avatar.html',
                         upload_form=upload_form, crop_form=crop_form)


@user_bp.route('/settings/avatar/upload', methods=['POST'])
@login_required
@confirm_required
def upload_avatar():
  form = UploadAvatarForm()
  if form.validate_on_submit():
    image = form.image.data
    filename = avatars.save_avatar(image)
    current_user.avatar_raw = filename
    db.session.commit()
    flash('Image upload, please crop.', 'success')
  flash_errors(form)
  return redirect(url_for('.change_avatar'))


@user_bp.route('/settings/avatar/crop', methods=['POST'])
def crop_avatar():
  form = CropAvatarForm()
  if form.validate_on_submit():
    x = form.x.data
    y = form.y.data
    w = form.w.data
    h = form.h.data
    filename = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
    current_user.avatar_s = filename[0]
    current_user.avatar_m = filename[1]
    current_user.avatar_l = filename[2]
    db.session.commit()
    flash('Avatar updated.', 'success')
  flash_errors(form)
  return redirect(url_for('.change_avatar'))


@user_bp.route('/settings/change-password', methods=['GET', 'POST'])
@fresh_login_required
def change_password():
  form = ChangePasswordForm()
  if form.validate_on_submit():
    if current_user.validate_password(form.old_password.data):
      current_user.set_password(form.password.data)
      db.session.commit()
      flash('Password updated.', 'success')
      return redirect(url_for('.index', username=current_user.username))
    else:
      flash('Old password is incorrect.', 'warning')
  return render_template('user/settings/change_password.html', form=form)


@user_bp.route('/setting/change-email', methods=['GET', 'POST'])
@fresh_login_required
def change_email_request():
  form = ChangeEmailForm()
  if form.validate_on_submit():
    token = generate_token(
      user=current_user, option=Operations.CHANGE_EMAIL,
      new_email=form.email.data.lower()
    )
    send_change_email(to=form.email.data, user=current_user.username, token=token)
    flash('Confirm email sent, check your inbox.', 'info')
    return redirect(url_for('.index', username=current_user.username))
  return render_template('user/settings/change_email.html', form=form)


@user_bp.route('/change-email/<token>')
@login_required
def change_email(token):
  if validate_token(user=current_user, token=token, operation=Operations.CHANGE_EMAIL):
    flash('Email updated.', 'success')
    return redirect(url_for('.index', username=current_user.username))
  else:
    flash('Invalid or expired token.', 'warning')
    return redirect(url_for('.change_email_request'))


@user_bp.route('/settings/notification', methods=['GET', 'POST'])
@login_required
def notification_setting():
  form = NotificationSettingForm()
  if form.validate_on_submit():
    current_user.receive_collect_notification = form.receive_collect_notification.data
    current_user.receive_follow_notification = form.receive_follow_notification.data
    current_user.receive_comment_notification = form.receive_comment_notification.data
    db.session.commit()
    flash('Notification settings updated.', 'success')
    return redirect(url_for('.index', username=current_user.username))
  form.receive_collect_notification = current_user.receive_collect_notification
  form.receive_follow_notification = current_user.receive_follow_notification
  form.receive_comment_notification = current_user.receive_comment_notification
  return render_template('user/settings/edit_notification.html', form=form)


@user_bp.route('/settings/privacy', methods=['GET', 'POST'])
@login_required
def privacy_setting():
  form = PrivacySettingForm()
  if form.validate_on_submit():
    current_user.public_collections = form.public_collections.data
    db.session.commit()
    flash('Privacy setting updated.', 'success')
    return redirect('.index', username=current_user.username)
  form.public_collections.data = current_user.public_collections
  return render_template('user/settings/edit_privacy.html', form=form)


@user_bp.route('/settings/account/delete', methods=['GET', 'POST'])
@fresh_login_required
def delete_account():
  form = DeleteAccountForm()
  if form.validate_on_submit():
    db.session.delete(current_user._get_current_object())
    db.session.commit()
    flash('You are free, goodbye!', 'success')
    return redirect(url_for('main.inex'))
  return render_template('user/settings/delete_account.html', form=form)