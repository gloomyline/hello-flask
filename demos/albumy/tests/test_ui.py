#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File    :   test_ui.py
@Time    :   2024/08/13 09:05:48
@Author  :   Alan
@Desc    :   None
'''
import time
import unittest
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from albumy.models import User
from albumy.settings import config


class UserInterfaceTestCase(unittest.TestCase):

  def setUp(self):
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    self.client = webdriver.Chrome(options=options)

    self.index_page = 'http://localhost:9898'
    # access to home page
    self.client.get(self.index_page)
    # wait page loading
    time.sleep(2)

    if not self.client:
      self.skipTest('Web browser not available.')

  def tearDown(self):
    if self.client:
      self.client.quit()

  def login(self):
    # access to login page
    self.client.find_element(By.LINK_TEXT, 'Login').click()
    time.sleep(1)
    # input username
    self.client.find_element(By.NAME, 'email').send_keys('admin@helloflask.com')
    # input password
    self.client.find_element(By.NAME, 'password').send_keys('12345678')
    # click login submit button
    self.client.find_element(By.ID, 'submit').click()
    time.sleep(1)

  def logout(self):
    self.client.find_element(By.ID, 'personal-dropdown').click()
    time.sleep(1)
    self.client.find_element(By.LINK_TEXT, 'Logout').click()
    time.sleep(1)

  def test_login(self):
    self.login()
    self.assertIn('Login success.', self.client.page_source)
    self.client.get_screenshot_as_file(
      f'{config['testing'].ALBUMY_UI_TEST_SCREENSHOTS_PATH} \
        /login_success.{uuid.uuid4().hex}.png'
    )

  def test_logout(self):
    self.login()
    self.logout()
    self.assertIn('Logout success.', self.client.page_source)

  def test_home_page(self):
    self.assertIn('Albumy', self.client.page_source)

    search = self.client.find_element(By.NAME, 'q')
    search.send_keys('Photo')
    search.send_keys(Keys.RETURN)
    self.assertIn('Photo', self.client.page_source)

    search = self.client.find_element(By.NAME, 'q')
    search.clear()
    search.send_keys('User')
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    self.client.find_element(By.LINK_TEXT, 'User').click()
    self.assertEqual(len(self.client.find_elements(By.CLASS_NAME, 'user-card')), 4)

    follow = self.client.find_element(
      By.XPATH,
      '/html/body/main/div/div[2]/div[2]/div[1]/form/button'
    )
    follow.click()
    time.sleep(2)
    self.assertIn('Please log in to access this page.', self.client.page_source)
    self.client.get_screenshot_as_file(f'{config['testing'].ALBUMY_UI_TEST_SCREENSHOTS_PATH}/ \
                                       login_required.{uuid.uuid4().hex}.png')

  def test_explore_page(self):
    self.client.find_element(By.LINK_TEXT, 'Explore').click()
    time.sleep(2)

    old_count = len(self.client.find_elements(By.CLASS_NAME, 'photo-card'))
    self.client.find_element(By.PARTIAL_LINK_TEXT, 'Change').click()
    time.sleep(1)
    new_count = len(self.client.find_elements(By.CLASS_NAME, 'photo-card'))
    self.assertEqual(old_count, new_count)

  def test_register(self):
    # maximize the window
    self.client.maximize_window()

    self.client.find_element(By.LINK_TEXT, 'Join Albumy').click()
    time.sleep(2)

    self.client.find_element(By.ID, 'name').send_keys('Test User')
    self.client.find_element(By.ID, 'email').send_keys('a1211071880@163.com')
    self.client.find_element(By.ID, 'username').send_keys('test')
    self.client.find_element(By.ID, 'password').send_keys('12345678')
    self.client.find_element(By.ID, 'password2').send_keys('12345678')
    self.client.find_element(By.ID, 'submit').click()
    time.sleep(2)
    self.assertIn('Confirm email sent, check your inbox.', self.client.page_source)
    self.client.get_screenshot_as_file(
      f'{config['testing'].ALBUMY_UI_TEST_SCREENSHOTS_PATH} \
       /register_send_email_confirm.{uuid.uuid4().hex}.png'
    )
    time.sleep(2)

    self.client.get('https://mail.163.com/')
    time.sleep(2)
    email_login_iframe = self.client.find_element(
      By.XPATH,
      '//*[@id="loginDiv"]/iframe'
    )
    # switch to iframe
    self.client.switch_to.frame(email_login_iframe)
    time.sleep(1)
    self.client.find_element(By.NAME, 'email').clear()
    time.sleep(0.5)
    self.client.find_element(By.NAME, 'email').send_keys('your email account')
    time.sleep(0.5)
    self.client.find_element(By.NAME, 'password').clear()
    time.sleep(0.5)
    self.client.find_element(By.NAME, 'password').send_keys('your email password')
    time.sleep(0.5)
    self.client.find_element(By.ID, 'dologin').click()
    
    
    # switch back to parent
    self.client.switch_to.parent_frame()
    time.sleep(2)

    def refresh_email():
      self.client.find_element(By.ID, '_mail_component_92_92').click()

    """
    TODO: mark it here, will implement in the future
    unread_email_num = self.client.find_element(By.CLASS_NAME, 'gWel-mailInfo-status').text

    if int(unread_email_num) > 0:
      self.client.find_element(By.ID, 'gWel-animMailcon').click()
      time.sleep(2)
      unread_emails = self.client.find_elements(By.CLASS_NAME, 'da0')
      for i in range(1, len(unread_emails)):
        email_name = self.client.find_elements(By.CLASS_NAME, 'da0')[i].text
        if email_name == '1211071880@qq.com':
          self.client.find_element(By.CLASS_NAME, 'da0').click()
          time.sleep(1)
          iframe = self.client.find_element(
            By.XPATH,
            '/html/body/div[2]/div[1]/div[3]/div/div[1]/div[6]/div/iframe'
          )
          self.client.switch_to.frame(iframe)
          time.sleep(1)
          res = self.client.find_element(
            By.CLASS_NAME,
            'netease_mail_readhtml.netease_mail_readhtml_webmail'
          ).text
    else:
      self.skipTest('not exsists unread emails')
    """

  