#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


def login(email, password):
    'login developer cloud'
    if not email or not password:
        raise ValueError('Please offer email and password.')

    session = requests.session()
    #1. Get conversations and authenticity_token
    try:
        step = 1
        msg = 'Get conversations and authenticity_token'

        resp = session.get(url='https://id.unity.com/en/login', verify=False)
        soup = BeautifulSoup(resp.text, 'html.parser')
        url = resp.url
        inputs = soup.find_all('input', attrs={'name': 'authenticity_token'})
        authenticity_token = inputs[0].attrs['value']
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #2. Sign in
    try:
        step = 2
        msg = 'Sign in'

        data = {
            'utf8': '✓',
            '_method': 'put',
            'authenticity_token': authenticity_token,
            'conversations_create_session_form[email]': email,
            'conversations_create_session_form[password]': password,
            'conversations_create_session_form[remember_me]': 'false',
            'commit': 'Sign in'
        }
        resp = session.post(url=url, data=data, verify=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #3. Start login developer cloud
    try:
        step = 3
        msg = 'Start login developer cloud'

        url = 'https://core.cloud.unity3d.com/api/login/start'
        params = {'redirect': 'https://developer.cloud.unity3d.com/projects/'}
        resp = session.get(url=url, params=params, verify=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #4. Get connect_token
    try:
        step = 4
        msg = 'Get connect_token'

        headers = {
            'Cookie': 'redirect=https://developer.cloud.unity3d.com/projects/'
        }
        ret = re.search(ur'window.location.href.+"(.+)"', resp.text)
        if not ret:
            raise ValueError('No valid URL.')
        url = ret.groups()[0]
        resp = session.get(
            url=url, headers=headers, verify=False, allow_redirects=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    return resp.headers['Set-Cookie']
