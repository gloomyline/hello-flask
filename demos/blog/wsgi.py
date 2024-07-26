#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   wsgi.py
@Time    :   2024/07/24 09:38:19
@Author  :   Alan
@Desc    :   None
'''

import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
  load_dotenv(dotenv_path)

from blog import create_app

app = create_app('production')