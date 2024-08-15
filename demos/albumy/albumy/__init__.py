#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   __init__.py
@Time    :   2024/07/26 14:26:22
@Author  :   Alan
@Desc    :   None
'''
import os
import click
from flask import Flask, render_template
from flask_login import current_user
from flask_wtf.csrf import CSRFError

from albumy.settings import config
from albumy.extensions import db, login_manager, bootstrap, moment, \
    mail, csrf, avatars, whooshee, dropzone, migrate, rich, debug_toolbar
from albumy.models import Collect, Comment, Follow, Notification, Photo, Role, Tag, User
from albumy.blueprints.main import main_bp
from albumy.blueprints.auth import auth_bp
from albumy.blueprints.user import user_bp
from albumy.blueprints.ajax import ajax_bp
from albumy.blueprints.admin import admin_bp


def create_app(config_name=None):
  if config_name is None:
    config_name = os.getenv('FLASK_ENV', 'development')

  app = Flask('albumy')

  app.config.from_object(config[config_name])

  register_extensions(app)
  register_blueprints(app)
  register_commands(app)
  register_errorhandlers(app)
  register_shell_context(app)
  register_template_context(app)
  return app


def register_extensions(app):
  db.init_app(app)
  login_manager.init_app(app)
  bootstrap.init_app(app)
  moment.init_app(app)
  mail.init_app(app)
  csrf.init_app(app)
  avatars.init_app(app)
  whooshee.init_app(app)
  dropzone.init_app(app)
  migrate.init_app(app, db)
  rich.init_app(app)
  debug_toolbar.init_app(app)


def register_blueprints(app):
  app.register_blueprint(main_bp)
  app.register_blueprint(auth_bp, url_prefix='/auth')
  app.register_blueprint(user_bp, url_prefix='/user')
  app.register_blueprint(ajax_bp, url_prefix='/api')
  app.register_blueprint(admin_bp, url_prefix='/admin')


def register_commands(app):
  @app.cli.command()
  @click.option('--drop', is_flag=True, help='Create after drop.')
  def initdb(drop):
    """Initialize the database."""
    if drop:
      click.confirm(
          click.style('This operation will delete the database, stll continue?', fg='bright_red'),
          abort=True
      )
      db.drop_all()
      click.echo(click.style('Drop tables.', fg='blue'))
    db.create_all()
    click.secho('Initialized database.', fg='bright_green')

  @app.cli.command()
  def init():
    """Initialize Albumy."""
    click.secho('Initialize the database...', fg='blue')
    db.create_all()
    click.secho('Initialize the roles and permissions...', fg='blue')
    Role.init_role()
    click.secho('Done.', fg='bright_green')

  @app.cli.command()
  @click.option('--user', default=10, help='Quantity of users, default is 10.')
  @click.option('--follow', default=30, help='Quantity of follows, default is 30.')
  @click.option('--photo', default=30, help='Quantity of photos, default is 30.')
  @click.option('--tag', default=20, help='Quantity of tags, default is 20.')
  @click.option('--collect', default=50, help='Quantity of collects, default is 50.')
  @click.option('--comment', default=100, help='Quantity of comments, default is 100.')
  def forge(user, follow, photo, tag, collect, comment):
    """Generate fake data."""
    from albumy.fakes import fake_admin, fake_comment, fake_follow, fake_photo, \
        fake_tag, fake_user, fake_collect
 
    db.drop_all()
    db.create_all()

    click.secho('Intializing the roles and permissions...', fg='bright_blue')
    Role.init_role()
    click.secho('Generating the administrator...', fg='cyan')
    fake_admin()
    click.secho('Generating %d users...' % user, fg='blue')
    fake_user(user)
    click.secho('Generating %d follows...' % follow, fg='bright_blue')
    fake_follow(follow)
    click.secho('Generating %d tags...' % tag, fg='cyan')
    fake_tag(tag)
    click.secho('Generating %d photos...' % photo, fg='blue')
    fake_photo(photo)
    click.secho('Generating %d collects...' % collect, fg='bright_blue')
    fake_collect(collect)
    click.secho('Generating %d comments...' % collect, fg='cyan')
    fake_comment(comment)
    click.secho('Done.', fg='green')


def register_errorhandlers(app):
  @app.errorhandler(400)
  def bad_request(e):
    return render_template('errors/400.html'), 400

  @app.errorhandler(403)
  def forbidden(e):
    return render_template('errors/403.html'), 403

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('errors/404.html'), 404

  @app.errorhandler(413)
  def request_entity_too_large(e):
    return render_template('errors/413.html'), 413

  @app.errorhandler(500)
  def internal_server_error(e):
    return render_template('errors/413.html'), 500

  @app.errorhandler(CSRFError)
  def handle_csrf_error(e):
    return render_template('errors/400.html', description=e.description), 500


def register_shell_context(app):
  @app.shell_context_processor
  def make_shell_context():
    return dict(db=db, User=User, Photo=Photo, Tag=Tag,
                Follow=Follow, Collect=Collect, Comment=Comment,
                Notification=Notification)


def register_template_context(app):
  @app.context_processor
  def make_template_context():
    if current_user.is_authenticated:
      """
      https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html
      Deprecated since version 2.0:
      The Query.with_parent() method is considered legacy as of the 1.x series of SQLAlchemy
      and becomes a legacy construct in 2.0. Use the with_parent() standalone construct.
      (Background on SQLAlchemy 2.0 at: SQLAlchemy 2.0 - Major Migration Guide)
      """
      # notification_count = Notification.query.with_parent(current_user).filter_by(is_read=False).count()
      notification_count = Notification.query.filter(
        Notification.is_read == False,
        db.orm.with_parent(current_user, User.notifications),
      ).count()
    else:
      notification_count = None
    return dict(notification_count=notification_count, is_development=app.config['DEBUG'])
