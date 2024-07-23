#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   views.py
@Time    :   2024/07/23 13:57:21
@Author  :   Alan
@Desc    :   None
'''

from flask import flash, redirect, render_template, url_for

from noteboard import app, db
from noteboard.models import Message
from noteboard.forms import BoardForm


@app.route('/', methods=['GET', 'POST'])
def index():
  messages = Message.query.order_by(Message.timestamp.desc()).all()
  form = BoardForm()
  if form.validate_on_submit():
    name = form.name.data
    body = form.body.data
    message = Message(name=name, body=body)
    db.session.add(message)
    db.session.commit()
    flash('Your message have been sent to the board!')
    return redirect(url_for('index'))
  return render_template('index.html', form=form, messages=messages)

@app.route('/del/<int:id>', methods=['POST'])
def remove(id):
  message = Message.query.get(id)
  if message is not None:
    db.session.delete(message)
    db.session.commit()
    flash('Delete message from %s successfully~' % message.name)
  else:
    flash('The message is not existed.')
  return redirect(url_for('index')) 
  