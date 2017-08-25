#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import time
import os
import requests
import login

ERROR_INVALID_TOKEN = 'Invalid Token'
ERROR_INVALID_DATA = 'Invalid Data'


def get_dau_from_cloud(token, app_id, start_date, end_date):
    'send request'
    headers = {'Cookie': token}
    cohort_metric_string = '[{"metric_name":"DAU","cohort_name":"All Current Users","graph_id":"0DAUAll Current Users","series":[],"type":"metric"}]'
    params = {
        'app_id': app_id,
        'cohort_metric_string[]': cohort_metric_string,
        'datepicker_start': start_date,
        'datepicker_end': end_date
    }
    url = 'https://analytics.cloud.unity3d.com/graph_service/get_graph_data.json'
    resp = requests.get(
        url=url, headers=headers, params=params, verify=False)
    json_data = json.loads(resp.text, encoding=resp.encoding)
    if json_data.has_key('redirectUrl') \
        or not json_data.has_key('cohort_metrics'):
        raise ValueError(ERROR_INVALID_TOKEN)

    try:
        series = json_data['cohort_metrics'][0]['series']
        dau = {}
        for tmp in series:
            day = time.strftime('%Y-%m-%d', time.localtime(tmp[0] / 1000.0))
            dau[day] = tmp[1] if tmp[1] else 0
        return dau
    except Exception, ex:
        raise ValueError(ERROR_INVALID_DATA + ':' + ex)


def init(email):
    dau_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'dau', email)
    if not os.path.exists(dau_dir):
        os.makedirs(dau_dir)
    return dau_dir


def get_token(dau_dir, email, password):
    token = None
    token_path = os.path.join(dau_dir, '.token')
    if os.path.exists(token_path):
        data = open(token_path)
        token = data.read()
        data.close()
    if not token:
        try:
            token = login.login(email, password)
            if token:
                data = open(token_path, 'w')
                data.write(token)
                data.close()
        except Exception, ex:
            print 'Get token failed. ', ex
    return token


def read_dau(dau_dir, app_id):
    dau_path = os.path.join(dau_dir, app_id + '.json')
    dau = {}
    if os.path.exists(dau_path):
        file_content = open(dau_path)
        json_data = json.loads(file_content.read())
        file_content.close()
        dau = json_data['dau']
    return dau


def save_dau(dau_dir, app_id, dau):
    dau_path = os.path.join(dau_dir, app_id + '.json')
    if os.path.exists(dau_path):
        old_dau = read_dau(dau_dir, app_id)
        dau = dict(old_dau, **dau)

    dau = {'dau': dau}
    file_content = open(dau_path, 'w')
    file_content.write(json.dumps(dau, indent=4, sort_keys=True))
    file_content.close()


def main(argv):
    'main'
    # if not argv:
    #     return
    email = ''
    password = ''
    app_id = ''

    dau_dir = init(email)
    token = get_token(dau_dir, email, password)
    if not token:
        return

    try:
        dau = get_dau_from_cloud(token, app_id, '08/22/2017', '08/26/2017')
        save_dau(dau_dir, app_id, dau)
    except ValueError, err:
        if ERROR_INVALID_TOKEN in err:
            print 'Delete .token and try again.'
        elif ERROR_INVALID_DATA in err:
            print 'Hmm... Check the json data in Charles.'


if __name__ == '__main__':
    try:
        requests.packages.urllib3.disable_warnings()
        main(sys.argv[1:])
    except Exception, ex:
        print ex
