#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   bundles.py
@Time    :   2024/08/15 13:51:18
@Author  :   Alan
@Desc    :   None
'''
from flask_assets import Environment, Bundle


assets = Environment()

css = Bundle('css/black_swan.min.css',
             'css/perfect_blue.min.css',
             'css/bootstrap.min.css',
             'css/dropzone.min.css',
             'css/style.css',
             filters='cssmin',
             output='gen/packed.css')

js = Bundle('js/jquery.min.js',
            'js/popper.min.js',
            'js/bootstrap.min.js',
            'js/dropzone.min.js',
            'js/moment-with-locales.min.js',
            'js/script.js',
            filters='jsmin',
            output='gen/packed.js')

assets.register('css_all', css)
assets.register('js_all', js)