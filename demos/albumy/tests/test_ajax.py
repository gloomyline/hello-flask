#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_ajax.py
@Time    :   2024/08/09 11:39:41
@Author  :   Alan
@Desc    :   test case of bp_ajax
'''
from flask import url_for
from flask_login import current_user

from tests.base import BaseTestCase
from albumy.models import User, Photo


class AjaxTestCase(BaseTestCase):

  def test_notifications_count(self):
    response = self.client.get(url_for('ajax.notifications_count'))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Login required.')

    self.login()
    response = self.client.get(url_for('ajax.notifications_count'))
    self.assertEqual(response.status_code, 200)
  
  def test_get_profile(self):
    response = self.client.get(url_for('ajax.get_profile', user_id=1))
    data = response.get_data(as_text=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn('Admin', data)

  def test_followers_count(self):
    user1 = User.query.get(1)
    user2 = User.query.get(2)
    user2.follow(user1)
    data = self.client.get(url_for('ajax.followers_count', user_id=1)).get_json()
    self.assertEqual(data['count'], 1)

  def test_collectors_count(self):
    response = self.client.get(url_for('ajax.collectors_count', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['count'], 0)

    user = User.query.get(1)
    user.collect(Photo.query.get(1))

    response = self.client.get(url_for('ajax.collectors_count', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['count'], 1)

  def test_my_collections_count(self):
    data = self.client.get(url_for('ajax.my_collections_count')).get_json()
    self.assertEqual(data['count'], 0)

    User.query.get(2).collect(Photo.query.get(1))
    self.login()
    data = self.client.get(url_for('ajax.my_collections_count')).get_json()
    self.assertEqual(data['count'], 1)

  def test_my_followings_count(self):
    data = self.client.get(url_for('ajax.my_followings_count')).get_json()
    self.assertEqual(data['count'], 0)

    User.query.get(2).follow(User.query.get(1))
    self.login()
    data = self.client.get(url_for('ajax.my_followings_count')).get_json()
    self.assertEqual(data['count'], 1)

  def test_collect(self):
    response = self.client.post(url_for('ajax.collect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Login required.')

    self.login(email='unconfirmed@helloflask.com', password='12345678')
    response = self.client.post(url_for('ajax.collect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Confirm account required.')
    self.logout()

    self.login()
    response = self.client.post(url_for('ajax.collect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['message'], 'Photo collected.')

    response = self.client.post(url_for('ajax.collect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['message'], 'Already collected.')

  def test_uncollect(self):
    response = self.client.post(url_for('ajax.uncollect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Login required.')

    self.login()
    response = self.client.post(url_for('ajax.uncollect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['message'], 'Not collected yet.')

    user = User.query.get(2)
    user.collect(Photo.query.get(1))

    response = self.client.post(url_for('ajax.uncollect', photo_id=1))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['message'], 'Photo uncollected.')


  def test_follow(self):
    response = self.client.post(url_for('ajax.follow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Login required.')

    self.login(email='unconfirmed@helloflask.com', password='12345678')
    response = self.client.post(url_for('ajax.follow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Confirm account required.')
    self.logout()

    self.login()
    response = self.client.post(url_for('ajax.follow', username='normal'))
    data = response.get_json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['message'], 'Already followed.')

    response = self.client.post(url_for('ajax.follow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['message'], 'User followed.')

  def test_unfollow(self):
    response = self.client.post(url_for('ajax.unfollow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 403)
    self.assertEqual(data['message'], 'Login required.')

    self.login()
    response = self.client.post(url_for('ajax.unfollow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['message'], 'Not followed yet.')

    user = User.query.get(2)
    user.follow(User.query.get(1))

    response = self.client.post(url_for('ajax.unfollow', username='admin'))
    data = response.get_json()
    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['message'], 'Follow canceled.')

