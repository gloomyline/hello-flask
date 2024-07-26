#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/07/23 19:09:03
@Author  :   Alan
@Desc    :   None
'''
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

import click
from flask import Flask, render_template, request
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from flask_sqlalchemy.record_queries import get_recorded_queries 

from blog.blueprints.auth import auth_bp
from blog.blueprints.essay import essay_bp
from blog.blueprints.admin import admin_bp
from blog.extensions import bootstrap, db, login_manager, moment, csrf, migrate, \
    ckeditor, mail, toolbar
from blog.models import Admin, Category, Link, Comment, Post
from blog.settings import config

basedir = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('FLASK_CONFIG', 'development')

  app = Flask('blog')
  app.config.from_object(config[config_name])

  register_logging(app)
  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errors(app)
  register_shell_context(app)
  register_template_context(app)
  register_request_handlers(app)
  return app


def register_logging(app):
  class RequestFormatter(logging.Formatter):

    def format(self, record):
      record.url = request.url
      record.remote_addr = request.remote_addr
      return super(RequestFormatter, self).format(record)

  request_formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
  )

  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  file_handler = RotatingFileHandler(
    os.path.join(basedir, 'logs/blog.log'),
    maxBytes=10 * 1024 * 1024,
    backupCount=10
  )
  file_handler.setFormatter(formatter)
  file_handler.setLevel(logging.INFO)

  mail_handler = SMTPHandler(
    mailhost = app.config['MAIL_SERVER'],
    fromaddr = app.config['MAIL_USERNAME'],
    toaddrs = ['ADMIN_EMAIL'],
    subject = 'Blog Application Error.',
    credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
  )
  mail_handler.setLevel(logging.ERROR)
  mail_handler.setFormatter(request_formatter)

  if not app.debug:
    app.logger.addHandler(mail_handler)
    app.logger.addHandler(file_handler)


def register_extensions(app):
  db.init_app(app)
  bootstrap.init_app(app)
  login_manager.init_app(app)
  moment.init_app(app)
  csrf.init_app(app)
  ckeditor.init_app(app)
  migrate.init_app(app, db)
  mail.init_app(app)
  toolbar.init_app(app)


def register_blueprints(app):
  app.register_blueprint(auth_bp)
  app.register_blueprint(essay_bp)
  app.register_blueprint(admin_bp)


def register_commands(app):
  @app.cli.command()
  @click.option('--drop', is_flag=True, help='Create after drop.')
  def initdb(drop):
    """Initialize Database."""
    if drop:
      click.confirm('This operation well %s the database, continue?' % click.style('delete', fg='red'), abort=True)
      db.drop_all()
      click.echo('Drop tables.')
    db.create_all()
    click.echo(click.style('Initialized database.', fg='green'))

  @app.cli.command()
  @click.option('--username', prompt=True, help='The username used to login.')
  @click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=True, help='The password used to login.')
  def init(username, password):
    """Building Blog, just for you."""
    click.echo('Initializing the database...')
    db.create_all()

    admin = Admin.query.first()
    if admin is not None:
      click.echo('The %s already exists, updating...' % click.style('administrator', fg='red'))
      admin.username = username
      admin.set_password(password) 
    else:
      click.echo('Creating the %s account...' % click.style('temporary administrator', fg='red'))
      admin = Admin(
        username = username,
        blog_title = 'Blog',
        blog_sub_title = 'No, I\'m real thing.',
        name = 'admin',
        about = 'Nothing.'
      )
      admin.set_password(password)
      db.session.add(admin)

    category = Category.query.first()
    if category is None:
      click.echo('Creating the %s...' % click.style('default category', fg='blue'))
      category = Category(name='Default')
      db.session.add(category)

    db.session.commit()
    click.echo(click.style('Done.', fg='green'))
  
  @app.cli.command()
  @click.option('--category', default=10, help='Quantity of categories, default is 10.')
  @click.option('--post', default=50, help='Quantity of posts, default is 50.')
  @click.option('--comment', default=500, help='Quantity of comments, default is 500.')
  def forge(category, post, comment):
    """Generate Fake data."""
    from blog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

    db.drop_all()
    db.create_all()

    click.echo('Generating the administrator...')
    fake_admin()

    click.echo('Generating %d categories...' % category)
    fake_categories(category)

    click.echo('Generating %d posts...' % post)
    fake_posts(post)

    click.echo('Generating %d comments...' % comment)
    fake_comments(comment)

    click.echo('Generating links...')
    fake_links()

    click.echo(click.style('Done.', fg='green'))


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_shell_context(app):
  @app.context_processor
  def make_sehll_context():
    return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
  @app.context_processor
  def make_template_context():
    admin = Admin.query.first()
    categories = Category.query.all()
    links = Link.query.order_by(Link.name).all()
    if current_user.is_authenticated:
      unread_commens = Comment.query.filter_by(reviewed=False).count()
      theme_name = current_user.theme or request.cookies.get('theme', 'perfect_blue')
    else:
      unread_commens = None
      theme_name = request.cookies.get('theme', 'perfect_blue')
    return dict(
      admin=admin,
      categories=categories,
      links=links,
      unread_commens=unread_commens,
      theme_name=theme_name
    ) 


def register_request_handlers(app):
  @app.after_request
  def query_profiler(response):
    for q in get_recorded_queries():
      if q.duration >= app.config['BLOG_SLOW_QUERY_THRESHOLD']:
        app.logger.warning(
          'Slow query: Duration: %fs\n Context: %s\n Query: %s\n'
          % (q.duration, q.context, q.statement)
        )
    return response