#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   commands.py
@Time    :   2024/07/23 15:19:05
@Author  :   Alan
@Desc    :   None
'''

import click

from noteboard import app, db
from noteboard.models import Message


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
  """Initialize the database."""
  if drop:
    click.confirm('This operation will delete the database, do you want to continue?', abort=True)
    db.drop_all()
    click.echo('Drop tables.')
  db.create_all()
  click.echo('Initialized database.')

@app.cli.command()
@click.option('--count', default=20, help='Quantity of messages, default is 20.')
def forge(count):
  """Generate fake messages."""
  from faker import Faker

  db.drop_all()
  db.create_all()

  fake = Faker()
  click.echo('Working...')

  for i in range(count):
    message = Message(
      name=fake.name(),
      body=fake.sentence(),
      timestamp=fake.date_time_this_year()
    )
    db.session.add(message)

  db.session.commit()
  click.echo('Created %d fake messages' % count)