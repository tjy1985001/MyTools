#!/usr/bin/env python
# -*- coding:utf-8 -*-
'Check Update'

import json
import sys
import time
import os
import getopt
import appstore
from appinfo import AppInfo

DATA_DIR = 'data/'
APP_INFO_SUFFIX = '.json'


def load_new_app_infos(apps_path):
    'retrieve new data from App Store'
    new_app_infos = appstore.lookup_from_file(apps_path)
    file_path = DATA_DIR + time.strftime('%Y-%m-%d %H.%M',
                                         time.localtime()) + APP_INFO_SUFFIX
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
    new_app_infos = load_new_app_infos(apps_path)
    old_app_infos = load_old_app_infos(old_data_path)
    print len(new_app_infos), len(old_app_infos)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
