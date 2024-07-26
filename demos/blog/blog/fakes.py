#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   fakes.py
@Time    :   2024/07/24 13:31:07
@Author  :   Alan
@Desc    :   None
'''
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from blog.extensions import db
from blog.models import Admin, Category, Comment, Post, Link


fake = Faker()


def fake_admin():
  admin = Admin(
    username='admin',    
    blog_title='Alanlog',
    blog_sub_title='No, I\'m real thing.',
    name='Alan Wang',
    about='Um, l, Alan Wang, have a fun time as a member of China...'
  )
  admin.set_password('admin@520')


def fake_categories(count=10):
  category = Category(name='Default')
  db.session.add(category)
  
  for i in range(count):
    category = Category(name=fake.word())
    db.session.add(category)
    try:
      db.session.commit()
    except IntegrityError:
      db.session.rollback()


def fake_posts(count=50):
  for i in range(count):
    post = Post(
      title=fake.sentence(),
      body=fake.text(1000),
      category=Category.query.get(random.randint(1, Category.query.count())),
      timestamp=fake.date_time_this_year()
    )
    db.session.add(post)
  db.session.commit()


def fake_comments(count=500):
  for i in range(count):
    comment = Comment(
      author=fake.name(),
      email=fake.email(),
      site=fake.url(),
      body=fake.sentence(),
      timestamp=fake.date_time_this_year(),
      reviewed=True,
      post=Post.query.get(random.randint(1, Post.query.count())),
    )
    db.session.add(comment)

  salt = int(count * 0.1)
  for i in range(salt):
    # unreviewed comments
    comment = Comment(
      author=fake.name(),
      email=fake.email(),
      site=fake.url(),
      body=fake.sentence(),
      timestamp=fake.date_time_this_year(),
      reviewed=False,
      post=Post.query.get(random.randint(1, Post.query.count())),
    )
    db.session.add(comment)
  
    # from admin
    comment = Comment(
      author=fake.name(),
      email=fake.email(),
      site=fake.url(),
      body=fake.sentence(),
      timestamp=fake.date_time_this_year(),
      from_admin=True,
      reviewed=True,
      post=Post.query.get(random.randint(1, Post.query.count())),
    )
    db.session.add(comment)
  db.session.commit()

  # replies 
  for i in range(salt):
    comment = Comment(
      author=fake.name(),
      email=fake.email(),
      site=fake.url(),
      body=fake.sentence(),
      timestamp=fake.date_time_this_year(),
      from_admin=True,
      reviewed=True,
      replied=Comment.query.get(random.randint(1, Comment.query.count())),
      post=Post.query.get(random.randint(1, Post.query.count())),
    )
    db.session.add(comment)
  db.session.commit()


def fake_links():
  twitter = Link(name='Twitter', url='https://x.com/')
  facebook = Link(name='Facebook', url='https://www.facebook.com/')
  linkedin = Link(name='Linkedin', url='https://www.linkedin.com/')
  google = Link(name='Google', url='https://www.google.com/')
  db.session.add_all([twitter, facebook, linkedin, google])
  db.session.commit()