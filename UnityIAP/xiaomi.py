#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import requests
from bs4 import BeautifulSoup
sys.path.append("..")
import UnityAnalytics.upid as upid


def get_app_info(package_name):
    url = 'http://app.mi.com/details?id=' + package_name
    resp = requests.get(url=url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    details = soup.select('div .details')[0].contents[0].contents
    current_version = details[3].contents[0]
    update_date = details[5].contents[0]
    app_id = details[9].contents[0]
    return {
        'package name': package_name,
        'app id': app_id,
        'current version': current_version,
        'update date': update_date
    }


def download_apk(package_name, app_id):
    url = 'http://app.mi.com/download/' + app_id
    apks_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'apks')
    if not os.path.exists(apks_dir):
        os.makedirs(apks_dir)
    apk_path = os.path.join(apks_dir, package_name + '.apk')
    try_count = 2
    while try_count > 0:
        try_count -= 1
        try:
            resp = requests.get(url=url, stream=True)
            file_content = open(apk_path, 'wb')
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    file_content.write(chunk)
            file_content.close()
            break
        except Exception, ex:
            print 'Got exception when downloading: ', ex
            file_content.close()
            os.remove(apk_path)
            if try_count == 0:
                apk_path = None
    return apk_path


def load_app_infos():
    pass


def save_app_infos():
    pass


def main():
    file_content = open('package_names.txt')
    app_infos = {}
    for line in file_content:
        package_name = line.strip()
        app_info = get_app_info(package_name)
        apk_path = download_apk(app_info['package name'], app_info['app id'])
        if not apk_path:
            print 'Download %s failed.' % package_name
            continue
        ua_info = upid.get_upid(apk_path)
        app_info['UPID'] = ua_info[2] if ua_info[2] else ua_info[3]
        app_infos[package_name] = app_info
        break
    file_content.close()
    file_content = open('apps.json', 'w')
    file_content.write(json.dumps(app_infos))
    file_content.close()


if __name__ == '__main__':
    main()
