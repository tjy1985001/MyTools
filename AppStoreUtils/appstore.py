#!/usr/bin/env python
# -*- coding:utf-8 -*-
'App Store Utils'

import json
import sys
import os
import codecs
import getopt
import requests
from appinfo import AppInfo

LOOK_UP_BASE_URL = 'https://itunes.apple.com/cn/lookup?'
BUNDLE_ID = 'bundle id'
APP_ID = 'app id'


def send_request(url):
    'send request'
    resp = requests.get(url=url)
    json_data = json.loads(resp.text, encoding=resp.encoding)
    if json_data['resultCount'] == 0:
        return None
    return json_data


def lookup(bundle_id, app_id):
    'retrieve data from App Store'
    print 'lookup: ', bundle_id, app_id
    json_data = None
    if app_id:
        json_data = send_request(LOOK_UP_BASE_URL + 'id=' + app_id)
    if bundle_id and not json_data:
        json_data = send_request(LOOK_UP_BASE_URL + 'bundleId=' + bundle_id)
    if not json_data:
        return None
    app_info = AppInfo(json_data)
    return app_info


def save_app_infos(app_infos, save_path):
    'save app infos to file as json'
    if not app_infos or not save_path:
        return
    try:
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        result = codecs.open(save_path, 'w', encoding='utf-8')
        app_infos = [app_info.__dict__ for app_info in app_infos]
        result.write(json.dumps(app_infos, indent=4, ensure_ascii=False))
        result.close()
    except Exception, ex:
        print 'save app infos failed.', ex


def lookup_from_configs(configs_path):
    'load bundle id and app id from file'
    app_infos = []
    try:
        configs_file = codecs.open(configs_path)
    except Exception, ex:
        print ex
        return app_infos

    configs = json.load(configs_file)
    configs_file.close()
    for config in configs['apps']:
        bundle_id = config[BUNDLE_ID] if config.has_key(BUNDLE_ID) else None
        app_id = config[APP_ID] if config.has_key(APP_ID) else None
        app_info = lookup(bundle_id, app_id)
        if app_info:
            app_infos.append(app_info)
        else:
            print 'lookup failed: %s, %s' % (bundle_id, app_id)
    return app_infos


def main(argv):
    'main'
    if not argv:
        return
    opts, args = getopt.getopt(argv, 'b:i:c:s:',
                               ['bundleId=', 'appId=', 'configs=', 'save='])
    bundle_id = app_id = configs_path = save_path = ''
    for opt, value in opts:
        if opt == '-b' or opt == '--bundleId':
            bundle_id = value
        elif opt == '-i' or opt == '--appId':
            app_id = value
        elif opt == '-c' or opt == '--configs':
            configs_path = value
        elif opt == '-s' or opt == '--save':
            save_path = value
    app_infos = None
    if configs_path:
        app_infos = lookup_from_configs(configs_path)
    else:
        app_info = lookup(bundle_id, app_id)
        if app_info:
            app_infos = [app_info]
    if app_infos:
        if save_path:
            save_app_infos(app_infos, save_path)
        for app_info in app_infos:
            app_info.output_info()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
