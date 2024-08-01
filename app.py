#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   app.py
@Time    :   2024/07/29 09:37:17
@Author  :   Alan
@Desc    :   simple app for practice
'''
import os
from flask import Flask


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
  app = Flask(__name__)
  return app