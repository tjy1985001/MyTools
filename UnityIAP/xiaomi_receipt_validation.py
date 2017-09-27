#!/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib
import requests

CLIENT_SECRET = ''
CLIENT_ID = ''


def validate(cp_order_id, order_query_token):
    sign_data = '%s&%s&%s&%s' % (CLIENT_ID, cp_order_id, order_query_token,
                                 CLIENT_SECRET)
    sign = hashlib.md5(sign_data).hexdigest()
    params = {
        'cpOrderId': cp_order_id,
        'clientId': CLIENT_ID,
        'orderQueryToken': order_query_token,
        'sign': sign
    }
    url = 'https://cn-api.unity.com/v1/order-attempts/query'
    resp = requests.get(url=url, params=params)
    print resp.content


def main():
    cp_order_id = ''
    order_query_token = ''
    validate(cp_order_id, order_query_token)


if __name__ == '__main__':
    main()
