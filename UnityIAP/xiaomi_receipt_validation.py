#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import requests

CLIENT_SECRET = ''
CLIENT_ID = ''

DEBUG_URL_VALIDATE_RECEIPT = 'https://cn-api-debug.unity.com/v1/order-attempts/query'
DEBUG_URL_VERIFY_LOGIN = 'https://cn-api-debug.unity.com/v1/login-attempts/verifyLogin'
URL_VALIDATE_RECEIPT = 'https://cn-api.unity.com/v1/order-attempts/query'
URL_VERIFY_LOGIN = 'https://cn-api.unity.com/v1/login-attempts/verifyLogin'


def validate_receipt(cp_order_id, order_query_token, is_debug):
    sign_data = '%s&%s&%s&%s' % (CLIENT_ID, cp_order_id, order_query_token, CLIENT_SECRET)
    sign = hashlib.md5(sign_data).hexdigest()
    params = {
        'cpOrderId': cp_order_id,
        'clientId': CLIENT_ID,
        'orderQueryToken': order_query_token,
        'sign': sign
    }
    url = DEBUG_URL_VALIDATE_RECEIPT if is_debug else URL_VALIDATE_RECEIPT
    resp = requests.get(url=url, params=params)
    return resp.json()


def verify_login(user_login_token, is_debug):
    sign_data = '%s&%s' % (user_login_token, CLIENT_SECRET)
    sign = hashlib.md5(sign_data).hexdigest()
    url = DEBUG_URL_VERIFY_LOGIN if is_debug else URL_VERIFY_LOGIN
    params = {'userLoginToken': user_login_token, 'sign': sign}
    resp = requests.get(url=url, params=params)
    return resp.json()


def main():
    cp_order_id = ''
    order_query_token = ''
    user_login_token = ''
    print validate_receipt(cp_order_id, order_query_token, False)
    print verify_login(user_login_token, True)


if __name__ == '__main__':
    main()
