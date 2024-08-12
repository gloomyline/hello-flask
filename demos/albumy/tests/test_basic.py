#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_basic.py
@Time    :   2024/08/08 16:35:36
@Author  :   Alan
@Desc    :   None
'''
from flask import current_app
from tests.base import BaseTestCase


class BasicTestCase(BaseTestCase):

  def test_app_exist(self):
    self.assertFalse(current_app is None)

  def test_app_is_testing(self):
    self.assertTrue(current_app.config['TESTING'])

  def test_404_error(self):
    response = self.client.get('/foo')
    data = response.get_data(as_text=True)
    self.assertEqual(response.status_code, 404)
    self.assertIn('404 Error', data)