#!/usr/bin/env python
# -*- coding:utf-8 -*-
'Check Update'

import json
import sys
import time
import codecs
import os
import getopt
import appstore
from appinfo import AppInfo

DATA_DIR = 'data/'
APP_INFO_SUFFIX = '.json'


def load_new_app_infos(apps_path, current_time):
    'retrieve new data from App Store'
    new_app_infos = appstore.lookup_from_file(apps_path)
    file_path = DATA_DIR + current_time + APP_INFO_SUFFIX
    appstore.save_app_infos(new_app_infos, file_path)
    return new_app_infos


def load_old_app_infos(old_data_path):
    'load old data from file'
    old_app_infos = []
    try:
        if not old_data_path or not os.path.exists(old_data_path):
            return old_app_infos
        json_data = json.loads(open(old_data_path).read())
        old_app_infos = [AppInfo(tmp) for tmp in json_data]
    except Exception, ex:
        print 'load_old_app_infos: ', ex
    return old_app_infos


def list2dict(apps):
    dic = {}
    for app in apps:
        dic[app.app_id] = app
    return dic


def compare(new_app_infos, old_app_infos):
    if not new_app_infos or not old_app_infos:
        return
    new_app_infos = list2dict(new_app_infos)
    old_app_infos = list2dict(old_app_infos)
    result = {'new': [], 'update': [], 'remove': []}
    for key in list(new_app_infos.keys()):
        value = new_app_infos[key]
        if old_app_infos.has_key(key):
            if not value == old_app_infos[key]:
                result['update'].append(value)
            new_app_infos.pop(key)
            old_app_infos.pop(key)
        else:
            result['new'].append(value)
            new_app_infos.pop(key)
    for key, value in old_app_infos.items():
        result['remove'].append(value)
    return result


def save_result(result, current_time, old_data_path):
    'save result to file as json'
    if not result or not current_time:
        return
    if not result['new'] and not result['update'] and not result['remove']:
        return
    try:
        save_path = DATA_DIR + 'diff-' + current_time + APP_INFO_SUFFIX
        dir_path = os.path.dirname(save_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        save_file = codecs.open(save_path, 'w', encoding='utf-8')
        for key in list(result.keys()):
            result[key] = [app_info.__dict__ for app_info in result[key]]
        result['old app infos path'] = old_data_path
        save_file.write(json.dumps(result, indent=4, ensure_ascii=False))
        save_file.close()
    except Exception, ex:
        print 'save result failed.', ex


def main(argv):
    'main'
    if not argv:
        return
    opts, args = getopt.getopt(argv, 'o:a:', ['old=', 'apps='])
    old_data_path = None
    apps_path = None
    for opt, value in opts:
        if opt == '-o' or opt == '--old':
            old_data_path = value
        elif opt == '-a' or opt == '--apps':
            apps_path = value
    current_time = time.strftime('%Y-%m-%d %H.%M', time.localtime())
    new_app_infos = load_new_app_infos(apps_path, current_time)
    if not old_data_path:
        return
    old_app_infos = load_old_app_infos(old_data_path)
    result = compare(new_app_infos, old_app_infos)
    save_result(result, current_time, old_data_path)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
