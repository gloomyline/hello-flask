# -*- coding: utf-8 -*-

import os

import click
from todoism.extensions import db
from mongoengine import connect


def register_commands(app):
  @app.cli.command()
  @click.option('--drop', is_flag=True, help='Create after drop.')
  def initdb(drop):
    """Initialize the database."""
    if drop:
      click.confirm('This operation will delete the database, do you want to continue?', abort=True)
      connect('todoism')
      db.drop_database('todoism')
      click.echo('Drop collections.')

  @app.cli.group()
  def translate():
    """Translation and localization commands."""
    pass

  @translate.command()
  @click.argument('locale')
  def init(locale):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o message.pot .'):
      raise RuntimeError('extract command failed.')
    if os.system('pybabel init -i message.pot -d todoism/translations -l' + locale):
      raise RuntimeError('init command failed.')
    os.remove('message.pot')

  @translate.command()
  def update():
    """Update a language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o message.pot .'):
      raise RuntimeError('extract command failed.')
    if os.system('pybabel update -i message.pot -d todoism/translations'):
      raise RuntimeError('update command failed.')
    os.remove('message.pot')

  @translate.command()
  def compile():
    """Compile a language."""
    if os.system('pybabel compile -d todoism/translations'):
      raise RuntimeError('compile command failed.')