#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   utils.py
@Time    :   2024/07/24 16:11:30
@Author  :   Alan
@Desc    :   None
'''
from urllib.parse import urljoin, urlparse
from flask import current_app, redirect, request, url_for


def is_safe_url(target):
  ref_url = urlparse(request.host_url)
  test_url = urlparse(urljoin(request.host_url, target))
  return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='essay.index', **kwargs):
  for target in request.args.get('next'), request.referrer:
    if not target:
      continue
    if is_safe_url(target):
      return redirect(target)
  return redirect(url_for(default, **kwargs))


def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in current_app.config['BLOG_ALLOWED_IMAGE_EXTENSIONS']