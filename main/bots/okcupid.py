#!/usr/bin/python
#-*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
# -- coding: utf-8 --
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import requests
import json
import os
import time
from datetime import datetime
from main.models import *


class Okcupid():

    BASE_URL = 'http://www.okcupid.com'
    LOGIN_URL = 'https://www.okcupid.com/login'
    USER_PAGE = 'http://www.okcupid.com/match'
    session = requests.Session()
    driver = webdriver.PhantomJS()  # Firefox() #
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.okcupid.com',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'
                 }
    cookies = None

    def __init__(self, username, password):

        self.username = username
        self.password = password
        # self.message = message

    def parse_requests_cookies(self, session_cookies):
        """ Parses requests' session cookies from into a dictionary """
        c = '%s' % session_cookies.__repr__
        c = c.split('Cookie(')
        cookies = []
        for x in c[1:]:
            x = x.strip('), ').split(', ')
            x = {i.split('=')[0]: i.split('=')[1].strip(
                "'").strip(')]>>') for i in x}
            cookies.append(x)
        return cookies

    def pass_cookies_to_selenium(self, driver):
        cookies = self.parse_requests_cookies(self.session.cookies)
        """ Adds the parsed cookies from requests into the selenium webdriver """
        for cookie in cookies:
            sc = {'name': '', 'value': '', 'path': '', 'domain': ''}
            for k, v in cookie.items():
                if k in sc.keys():
                    sc[k] = v
                    # if k == 'domain' and v.startswith('.'):
                    #   sc[k] = v[1:]
            driver.add_cookie(sc)

    def login(self):
        """ Login to the website using the specified credentials """

        # Post payload
        payload = {
                     'username': self.username,
                    'password': self.password
                  }
        response = self.session.post(self.LOGIN_URL, data=payload)

        # Check response
        if response.ok and 'home' in response.url:
            self.Cookie = self.session.cookies
            return True
        return False

    def message_user(self, message):

        self.driver.get(self.LOGIN_URL)
        self.pass_cookies_to_selenium(self.driver)
        self.driver.get(self.USER_PAGE)
        response = self.driver.page_source
        # response = self.session.get(self.USER_PAGE,headers=self.headers,cookies=self.Cookie)
        # fp = open('output','w')
        # fp.write(response.encode('ascii','ignore'))
        # fp.close()
        soup = BeautifulSoup(response, "html5lib")
        results = soup.find('div', {'class': 'match-results-cards'}).findAll(
            'div', {'class': 'match_card_wrapper user-not-hidden'})
        USERS = []
        for user in results:
            # print user.find('a')['href']
            USERS.append(self.BASE_URL + user.find('a')['href'])

        rand_user = random.choice(USERS)
        # print rand_user

        # Now open this user profile and send message
        response = self.session.get(rand_user)
        soup = BeautifulSoup(response.text, "html5lib")
        userid = soup.find('input', {'name': 'object_id'}).attrs['value']
        token = soup.find('input', {'name': 'authcode'}).attrs['value']
        username = soup.find('input', {'name': 'name'}).attrs['value']
        # print userid,token

        print 'Sending message to ' + username
        data = {"body": message, "only_messaging_group": "", "panel_group": "", "profile_tab": "profile",
                 "receiverid": userid,
                "reply": 0,
                "service": "profile",
             "source": "desktop_global"
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = self.session.post(
            'http://www.okcupid.com/apitun/messages/send?&access_token=' + token, data=json.dumps(data), headers=headers)
        # print response.text
        # print username
        fp = open('/root/user/main/bots/report.log', 'a')
        try:
            if response.json()['success'] == 1:
                print (time.strftime("%d/%m/%Y %H:%M:%S")) + " : Message sent to " + username
                fp.write('\n' + (time.strftime("%d/%m/%Y %H:%M:%S")) + " : Message sent to " + username)
            else:
                fp.write('\n' + (time.strftime("%d/%m/%Y %H:%M:%S")) +	" : Unable to send message to " + username + "Reason:" + response.text)
        except Exception as ex:
            fp.write('\n'+(time.strftime("%d/%m/%Y %H:%M:%S")) + " Error :  "+ ex)

        fp.close()
			


    def __del__(self):
	pass
        # self.driver.quit()

username =''
password = ''
O = Okcupid(username,password)
if O.login():
    print 'successful login'
    while True:
		timer = MessageSetting.objects.get(username=username).interval
		message = MessageSetting.objects.get(username=username).body
		O.message_user(message)
		time.sleep(timer)
