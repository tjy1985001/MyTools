#!/usr/bin/env python
# -*- coding:utf-8 -*-
'auto job'

import os
import time
import sys
import json
import check
sys.path.append(os.path.dirname(__file__) + "/..")
import PyCommon.emailutils as email

CONFIGS_NAME = 'configs.json'


def main():
    'main'
    configs_path = os.path.join(os.path.dirname(__file__), CONFIGS_NAME)
    configs_file = open(configs_path)
    configs = json.load(configs_file)
    configs_file.close()

    data_dir = os.path.join(os.path.dirname(__file__), configs['data dir'])
    file_names = os.listdir(data_dir)
    time_format = '%Y-%m-%d %H.%M'
    times = [
        time.strptime(name.replace('.json', ''), time_format)
        for name in file_names
        if name.endswith('.json') and not name.startswith('diff')
    ]
    times = sorted(times, reverse=True)
    file_name = time.strftime(time_format, times[0]) + '.json'
    diff_file_path = check.check(configs_path,
                                 os.path.join(data_dir, file_name))
    if diff_file_path:
        diff_file = open(diff_file_path)
        email.send_email(configs['mail_host'], configs['mail_user'],
                         configs['mail_pwd'], configs['to_addrs'],
                         'iOS App Store Update', diff_file.read())
        diff_file.close()


if __name__ == '__main__':
    try:
        main()
    except Exception, ex:
        print ex
