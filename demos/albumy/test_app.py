#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_app.py
@Time    :   2024/08/13 10:47:58
@Author  :   Alan
@Desc    :   test ui app(test) server
'''
from albumy import create_app, db
from albumy.models import User, Role, Photo, Comment, Tag


app = create_app('testing')

with app.app_context():
  db.create_all()
  Role.init_role()

  admin_user = User(email='admin@helloflask.com', name='Admin', username='admin', confirmed=True, active=True, role_id=4)
  admin_user.set_password('12345678')
  normal_user = User(email='normal@helloflask.com', name='Normal User', username='normal', confirmed=True, active=True, role_id=2)
  normal_user.set_password('12345678')
  unconfirmed_user = User(email='unconfirmed@helloflask.com', name='Unconfirmed User', username='unconfirmed',
                          confirmed=False, active=True)
  unconfirmed_user.set_password('12345678')
  locked_user = User(email='locked@helloflask.com', name='Locked User', username='locked',
                      confirmed=True, locked=True, active=True, role_id=1)
  locked_user.set_password('12345678')
  locked_user.lock()

  blocked_user = User(email='blocked@helloflask.com', name='Blocked User', username='blocked',
                      confirmed=True, active=False)
  blocked_user.set_password('12345678')

  photo = Photo(filename='test.jpg', filename_s='test_s.jpg', filename_m='test_m.jpg',
                description='Photo 1', author=admin_user)
  photo2 = Photo(filename='test2.jpg', filename_s='test_s2.jpg', filename_m='test_m2.jpg',
                  description='Photo 2', author=normal_user)

  comment = Comment(body='test comment body', photo=photo, author=normal_user)
  tag = Tag(name='test tag')
  photo.tags.append(tag)

  db.session.add_all([admin_user, normal_user, unconfirmed_user, locked_user, blocked_user, photo, photo2, comment, tag])
  db.session.commit()

