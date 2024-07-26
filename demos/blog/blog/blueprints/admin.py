#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   admin.py
@Time    :   2024/07/24 16:55:45
@Author  :   Alan
@Desc    :   None
'''
import os
from datetime import UTC, datetime

from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from flask_ckeditor import upload_success, upload_fail

from blog.extensions import db
from blog.forms import CategoryForm, PostForm, LinkForm, SettingsForm
from blog.models import Category, Comment, Link, Post
from blog.utils import allowed_file, redirect_back

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage')
@login_required
def manage_post():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', current_app.config['BLOG_MANAGE_POST_PER_PAGE'], type=int)
  pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
  posts = pagination.items
  return render_template('admin/manage_post.html', posts=posts, page=page, pagination=pagination)


@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    title = form.title.data
    body = form.body.data
    category = Category.query.get(form.category.data)
    post = Post(title=title, body=body, category=category)
    db.session.add(post)
    db.session.commit()
    flash('Post created.', 'success')
    return redirect(url_for('essay.show_post', post_id=post.id))
  return render_template('admin/new_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/set-comment', methods=['POST'])
@login_required
def set_comment(post_id):
  post = Post.query.get_or_404(post_id)
  if post.can_comment:
    post.can_comment = False
    flash('Comment disabled', 'success')
  else:
    post.can_comment = True 
    flash('Comment enabled', 'success')
  db.session.commit()
  return redirect_back()


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
  post = Post.query.get_or_404(post_id)
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.category = Category.query.get_or_404(form.category.data)
    post.body = form.body.data
    post.timestamp = datetime.now(UTC)
    db.session.commit()
    flash('Updated post', 'success')
    return redirect(url_for('essay.show_post', post_id=post.id))
  form.title.data = post.title
  form.category.data = post.category_id
  form.body.data = post.body
  return render_template('admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  db.session.delete(post)
  db.session.commit()
  flash('Deleted post.', 'success')
  return redirect_back()


@admin_bp.route('/category/manage')
@login_required
def manage_category():
  return render_template('admin/manage_category.html')


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
  form = CategoryForm()
  if form.validate_on_submit():
    name = form.name.data
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    flash('Created category~', 'success')
    return redirect(url_for('.manage_category'))
  return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
  category = Category.query.get_or_404(category_id)
  form = CategoryForm()
  if form.validate_on_submit():
    category.name = form.name.data
    db.session.commit()
    flash('Updated category.', 'success')
  form.name.data = category.name
  return render_template('admin/edit_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
  category = Category.query.get_or_404(category_id)
  # db.session.delete(category)
  # db.session.commit()
  category.delete()
  flash('Deleted category', 'success')
  return redirect_back()


@admin_bp.route('/comment/manage')
@login_required
def manage_comment():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', current_app.config['BLOG_MANAGE_POST_PER_PAGE'], type=int)
  filter_rule = request.args.get('filter', 'all') # 'all', 'unread' and 'admin'
  if filter_rule == 'unread':
    filtered_comments = Comment.query.filter(Comment.reviewed==False)
  elif filter_rule == 'admin':
    filtered_comments = Comment.query.filter_by(from_admin=True)
  else:
    filtered_comments = Comment.query
  pagination = filtered_comments \
    .order_by(Comment.timestamp.desc()) \
    .paginate(page=page, per_page=per_page)
  comments = pagination.items
  return render_template('admin/manage_comment.html', comments=comments, page=page, pagination=pagination)


@admin_bp.route('/comment/<int:comment_id>/approve', methods=['POST'])
@login_required
def approve_comment(comment_id):
  comment = Comment.query.get_or_404(comment_id)
  comment.reviewed = True
  db.session.commit()
  flash('Comment published', 'success')
  return redirect_back()


@admin_bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
  comment = Comment.query.get_or_404(comment_id)
  db.session.delete(comment)
  db.session.commit()
  flash('Comment deleted', 'success')
  return redirect_back()


@admin_bp.route('/link/manage')
@login_required
def manage_link():
  return render_template('admin/manage_link.html')

@admin_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
  form = LinkForm()
  if form.validate_on_submit():
    name = form.name.data
    url = form.url.data
    link = Link(name=name, url=url)
    db.session.add(link)
    db.session.commit()
    flash('Created Link.', 'success')
    return redirect(url_for('.manage_link'))
  return render_template('admin/new_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
  link = Link.query.get_or_404(link_id)
  form = LinkForm()
  if form.validate_on_submit():
    link.name = form.name.data
    link.url = form.url.data
    db.session.commit()
    flash('Updated Link', 'success')
    return redirect(url_for('.manage_link'))
  form.name.data = link.name
  form.url.data = link.url
  return render_template('admin/edit_link.html', form=form)


@admin_bp.route('/link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
  link = Link.query.get_or_404(link_id)
  db.session.delete(link)
  db.session.commit()
  flash('Deleted link.', 'success')
  return redirect(url_for('.manage_link'))


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
  form = SettingsForm()
  if form.validate_on_submit():
    current_user.name = form.name.data
    current_user.blog_title = form.blog_title.data
    current_user.blog_sub_title = form.blog_sub_title.data
    current_user.about = form.about.data
    db.session.commit()
    flash('Settings updated.', 'success')
    return redirect(url_for('essay.index'))
  form.name.data = current_user.name
  form.blog_title.data = current_user.blog_title
  form.blog_sub_title.data = current_user.blog_sub_title
  form.about.data = current_user.about
  return render_template('admin/settings.html', form=form)


@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
  f = request.files.get('upload')
  if not allowed_file(f.filename):
    return upload_fail('image only~')
  f.save(os.path.join(current_app.config['BLOG_UPLOAD_PATH'], f.filename))
  url = url_for('.get_image', filename=f.filename)
  return upload_success(url, f.filename)


@admin_bp.route('/uploads/<path:filename>')
def get_image(filename):
  return send_from_directory(current_app.config['BLOG_UPLOAD_PATH'], filename)