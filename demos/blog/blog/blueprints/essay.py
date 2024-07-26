#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   essay.py
@Time    :   2024/07/24 11:46:08
@Author  :   Alan
@Desc    :   None
'''
from flask import Blueprint, abort, current_app, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user

from blog.extensions import db
from blog.models import Admin, Category, Comment, Post
from blog.forms import AdminCommentForm, CommentForm
from blog.utils import redirect_back
from blog.emails import send_new_comment_email, send_new_reply_email

essay_bp = Blueprint('essay', __name__)


@essay_bp.route('/')
def index():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', current_app.config['BLOG_POST_PER_PAGE'], type=int)
  pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
  posts = pagination.items
  return render_template('essay/index.html', pagination=pagination, posts=posts)


@essay_bp.route('/about')
def about():
  return render_template('essay/about.html')


@essay_bp.route('/category/<int:category_id>')
def show_category(category_id):
  category = Category.query.get_or_404(category_id)
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', current_app.config['BLOG_POST_PER_PAGE'], type=int)
  pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page)
  posts = pagination.items
  return render_template('essay/category.html', category=category, pagination=pagination, posts=posts)


@essay_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
  post = Post.query.get_or_404(post_id)
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', current_app.config['BLOG_POST_PER_PAGE'], type=int)
  pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.desc()).paginate(page=page, per_page=per_page)
  comments = pagination.items

  if current_user.is_authenticated:
    form = AdminCommentForm()
    form.author.data = current_user.name
    form.email.data = current_app.config['BLOG_EMAIL']
    form.site.data = url_for('.index')
    from_admin = True
    reviewed = True
  else:
    form = CommentForm()
    from_admin = False
    reviewed = False

  if form.validate_on_submit():
    author = form.author.data
    email = form.email.data
    site = form.site.data
    body = form.body.data
    comment = Comment(
      author=author,
      email=email,
      site=site,
      body=body,
      post=post,
      from_admin=from_admin,
      reviewed=reviewed
    )
    replied_id = request.args.get('reply')
    if replied_id:
      replied_comment = Comment.query.get_or_404(replied_id)
      comment.replied = replied_comment
      # send notification email that his comment has been replied to the comment author
      send_new_reply_email(replied_comment)
    db.session.add(comment)
    db.session.commit()
    if current_user.is_authenticated:
      flash('Comment published.', 'success')
    else:
      flash('Thanks, your comment will be published after reviewed.', 'info')
      # send notification email to admin
      send_new_comment_email(post) 
    return redirect(url_for('.show_post', post_id=post_id))
  return render_template('essay/post.html', pagination=pagination, post=post, comments=comments, form=form)


@essay_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
  comment = Comment.query.get_or_404(comment_id)
  if not comment.post.can_comment:
    return redirect(url_for('.show_post', post_id=comment.post.id))
  return redirect(
    url_for(
      '.show_post',
      post_id=comment.post.id,
      reply=comment_id,
      author=comment.author
    ) + '#comment-form'
  )


@essay_bp.route('/theme/<string:theme_name>')
def change_theme(theme_name):
  if theme_name not in current_app.config['BLOG_THEMES'].keys():
    abort(404)
  response = make_response(redirect_back())
  if current_user.is_authenticated:
    admin = Admin.query.get_or_404(current_user.id)
    admin.theme = theme_name
    db.session.commit()
  else:
    response.set_cookie('theme', theme_name, max_age = 30 * 24 * 60 * 60)
  return response