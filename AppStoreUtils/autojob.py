#!/usr/bin/env python
# -*- coding:utf-8 -*-
'auto job'

import os
import time
import sys
import check
sys.path.append("..")
import PyCommon.emailutils as email

TO_ADDRS = ['']
MAIL_HOST = ''
MAIL_USER = ''
MAIL_PWD = ''


def main():
    'main'
    work_dir = os.path.dirname(__file__)
    if work_dir:
        os.chdir(work_dir)
    file_names = os.listdir('data')
    time_format = '%Y-%m-%d %H.%M'
    times = [
        time.strptime(name.replace('.json', ''), time_format)
        for name in file_names
        if name.endswith('.json') and not name.startswith('diff')
    ]
    times = sorted(times, reverse=True)
    file_name = time.strftime(time_format, times[0]) + '.json'
    file_path = check.check('data/apps.txt', 'data/' + file_name)
    if file_path:
        content = file(file_path)
        email.send_email(MAIL_HOST, MAIL_USER, MAIL_PWD, TO_ADDRS,
                         'iOS App Store Update', content.read())
        content.close()


if __name__ == '__main__':
    try:
        main()
    except Exception, ex:
        print ex
