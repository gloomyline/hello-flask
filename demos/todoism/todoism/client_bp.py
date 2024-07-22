#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   client_bp.py
@Time    :   2024/07/22 14:21:57
@Author  :   Alan
@Desc    :   None
'''

from flask import Blueprint, jsonify, redirect, render_template


client_bp = Blueprint('client_bp', __name__,
  # template_folder='template'
  static_folder='static',
  static_url_path=''
)

@client_bp.route('/')
def index():
  return client_bp.send_static_file('index.html'), 200
  # return render_template('index.html')
  # return jsonify('test')

@client_bp.route('/static/')
def index_static():
  return redirect('/')