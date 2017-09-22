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


def get_new_app_infos(configs_path, new_infos_path):
    'retrieve new data from App Store'
    new_app_infos = appstore.lookup_from_configs(configs_path)
    appstore.save_app_infos(new_app_infos, new_infos_path)
    return new_app_infos


def load_old_app_infos(old_data_path):
    'load old data from file'
    old_app_infos = []
    try:
        if not old_data_path or not os.path.exists(old_data_path):
            return old_app_infos
        app_infos_file = open(old_data_path)
        app_infos = json.load(app_infos_file)
        app_infos_file.close()
        old_app_infos = [AppInfo(tmp) for tmp in app_infos]
    except Exception, ex:
        print 'load_old_app_infos: ', ex
    return old_app_infos


def list2dict(apps):
    'convert list to dict. Key is app id'
    dic = {}
    for app in apps:
        dic[app.app_id] = app
    return dic


def compare(new_app_infos, old_app_infos):
    'compare new infos with old infos, and return the result.'
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


def save_result(result, diff_infos_path, old_data_path):
    'save result to file as json'
    if not result or not diff_infos_path:
        return None
    if not result['new'] and not result['update'] and not result['remove']:
        return None
    try:
        dir_path = os.path.dirname(diff_infos_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        save_file = codecs.open(diff_infos_path, 'w', encoding='utf-8')
        for key in list(result.keys()):
            result[key] = [app_info.__dict__ for app_info in result[key]]
        result['old app infos path'] = old_data_path
        save_file.write(json.dumps(result, indent=4, ensure_ascii=False))
        save_file.close()
        return diff_infos_path
    except Exception, ex:
        print 'save result failed.', ex


def check(configs_path, old_data_path):
    if not configs_path:
        return None
    configs_file = open(configs_path)
    configs = json.load(configs_file)
    configs_file.close()
    data_dir = os.path.join(os.path.dirname(__file__), configs['data dir'])
    file_name = time.strftime('%Y-%m-%d %H.%M', time.localtime()) + '.json'
    new_infos_path = os.path.join(data_dir, file_name)
    new_app_infos = get_new_app_infos(configs_path, new_infos_path)
    if not old_data_path:
        return None
    old_app_infos = load_old_app_infos(old_data_path)
    diff_infos = compare(new_app_infos, old_app_infos)
    if diff_infos:
        diff_infos_path = os.path.join(data_dir, 'diff-' + file_name)
        return save_result(diff_infos, diff_infos_path, old_data_path)
    return None


def main(argv):
    'main'
    if not argv:
        return
    opts, args = getopt.getopt(argv, 'o:c:', ['old=', 'configs='])
    old_data_path = None
    configs_path = None
    for opt, value in opts:
        if opt == '-o' or opt == '--old':
            old_data_path = value
        elif opt == '-c' or opt == '--configs':
            configs_path = value
    checked_path = check(configs_path, old_data_path)
    if checked_path:
        print 'The compared result was saved in %s' % checked_path


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
