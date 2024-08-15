#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/07/29 11:40:17
@Author  :   Alan
@Desc    :   None
'''
import os
import uuid
import PIL

from PIL import Image
from urllib.parse import urljoin, urlparse
import PIL.Image
from flask_login import current_user
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import URLSafeSerializer as Serializer 
from flask import current_app, flash, redirect, request, url_for

from albumy.settings import Operations
from albumy.extensions import db, cache
from albumy.models import User


def is_login():
  return current_user.is_authenticated


def generate_token(user, operation, expire_in=None, **kwargs):
  s = (
    Serializer(current_app.config['SECRET_KEY']),
    Serializer(current_app.config['SECRET_KEY'], expire_in)
  )[expire_in is not None]

  data = {'id': user.id, 'operation': operation}
  data.update(**kwargs)
  token = s.dumps(data)
  return token


def validate_token(user, token, operation, new_password=None):
  s = Serializer(current_app.config['SECRET_KEY'])

  try:
    data = s.loads(token)
  except (BadSignature, SignatureExpired):
    return False

  if operation != data.get('operation') or user.id != data.get('id'):
    return False

  if operation == Operations.CONFIRM:
    user.confirmed = True
  elif operation == Operations.RESET_PASSWORD:
    user.set_password(new_password)
  elif operation == Operations.CHANGE_EMAIL:
    new_email = data.get('new_email')
    if new_email is None:
      return False
    if User.query.filter_by(email=new_email).first() is not None:
      return False
    user.email = new_email
  
  db.session.commit()
  return True


def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
  for target in request.args.get('next'), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return redirect(target)
  return redirect(url_for(default, **kwargs))


def rename_image(old_filename):
  ext = os.path.splitext(old_filename)[1]
  new_filename = uuid.uuid4().hex + ext
  return new_filename


def resize_image(image, filename, base_width):
  filename, ext = os.path.splitext(filename)
  img = Image.open(image)
  if img.size[0] <= base_width:
    return filename +ext
  w_percent = (base_width / float(img.size[0]))
  h_size = int(float(img.size[1]) * float(w_percent))
  img = img.resize((base_width, h_size), PIL.Image.Resampling.LANCZOS)

  filename += current_app.config['ALBUMY_PHOTO_SUFFIX'][base_width] + ext
  img.save(
    os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename),
    optimize=True, quantity=50
  )
  return filename


def flash_errors(form):
  for field, errors in form.errors.items():
    for error in errors:
      flash(u'Error in the %s field - %s' % (
        getattr(form, field).label.text,
        error
      ))


def clear_cache(keys):
  for key in keys:
    cache.delete(key)