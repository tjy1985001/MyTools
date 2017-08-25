#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup


def login(email, password):
    'login developer cloud'
    if not email or not password:
        raise ValueError('Please offer email and password.')

    #1. Get conversations and authenticity_token
    try:
        step = 1
        msg = 'Get conversations and authenticity_token'

        resp = requests.get(url='https://id.unity.com/en/login', verify=False)
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
        headers = {'Cookie': resp.headers['Set-Cookie']}
        resp = requests.post(
            url=url,
            data=data,
            headers=headers,
            verify=False,
            allow_redirects=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #3. Get ss and ls
    try:
        step = 3
        msg = 'Get ss and ls'

        resp = requests.get(
            url=resp.headers['Location'],
            headers=headers,
            verify=False,
            allow_redirects=False)
        ss_and_ls = resp.headers['Set-Cookie']
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #4. Continue
    try:
        step = 4
        msg = 'Continue'

        url = get_location(resp)
        resp = requests.get(url=url, headers=headers, verify=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #5. Start login developer cloud
    try:
        step = 5
        msg = 'Start login developer cloud'

        url = 'https://core.cloud.unity3d.com/api/login/start'
        params = {'redirect': 'https://developer.cloud.unity3d.com/projects/'}
        resp = requests.get(
            url=url, params=params, verify=False, allow_redirects=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #6. Use ss and ls
    try:
        step = 6
        msg = 'Use ss and ls'

        headers = {'Cookie': ss_and_ls}
        resp = requests.get(
            url=resp.headers['Location'],
            headers=headers,
            verify=False,
            allow_redirects=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    #7. Get connect_token
    try:
        step = 7
        msg = 'Get connect_token'

        headers = {
            'Cookie': 'redirect=https://developer.cloud.unity3d.com/projects/'
        }
        url = get_location(resp)
        resp = requests.get(
            url=url, headers=headers, verify=False, allow_redirects=False)
    except Exception, ex:
        print 'Step #%d failed: %s. Exception: %s' % (step, msg, ex)
        return None

    return resp.headers['Set-Cookie']


def get_location(resp):
    'get redirect location'
    url = None
    if resp.status_code == 302:
        url = resp.headers['Location']
    elif resp.status_code == 200:
        ret = re.search(ur'window.location.href.+"(.+)"', resp.text)
        if ret:
            url = ret.groups()[0]
    if not url:
        raise ValueError('No valid URL.')
    return url
