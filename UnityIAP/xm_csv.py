#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
APP_NAME, BUNDLEID, APPID, GENRE_XIAOMI, GENRE_GOOGLEPLAY
'''

import os
import json
import sys
import time
import codecs
import unicodecsv as csv
sys.path.append(os.path.dirname(__file__) + "/..")
from GoogleTools.gplay import GooglePlay
from GoogleTools.drive import GoogleDrive
import PyCommon.emailutils as email

CONFIGS = {}


def init_configs():
    global CONFIGS
    configs_path = os.path.join(os.path.dirname(__file__), 'configs.json')
    configs_file = open(configs_path)
    CONFIGS = json.load(configs_file)
    configs_file.close()


def get_package_names():
    xm_gp = {}
    for package_name in CONFIGS['package_names']:
        xm_gp[package_name['xiaomi']] = package_name['google_play']
    return xm_gp


def get_xiaomi_apps():
    apps_path = os.path.join(os.path.dirname(__file__), 'data/apps.json')
    apps_file = open(apps_path)
    xm_apps = json.load(apps_file)
    apps_file.close()
    return xm_apps


def gen_csv(xm_apps, xm_gp):
    fields = [
        'APP_NAME', 'BUNDLEID', 'APPID', 'GENRE_XIAOMI', 'GENRE_GOOGLEPLAY'
    ]
    csv_name = time.strftime('%Y-%m-%d %H.%M', time.localtime()) + '.csv'
    csv_path = os.path.join(os.path.dirname(__file__), 'data', csv_name)
    csv_file = open(csv_path, 'wb')
    csv_file.write(codecs.BOM_UTF8)
    writer = csv.DictWriter(csv_file, fieldnames=fields)
    writer.writeheader()
    for xm in xm_apps:
        app = {}
        gp = GooglePlay(xm_gp[xm['package name']])
        app['BUNDLEID'] = xm['package name']
        app['APP_NAME'] = '%s(%s)' % (xm['app name'], gp.app_title)
        app['APPID'] = xm['UPID']
        app['GENRE_XIAOMI'] = xm['genre']
        app['GENRE_GOOGLEPLAY'] = gp.genre
        writer.writerow(app)
    csv_file.close()
    return csv_path


def upload_csv(csv_path):
    folder_id = CONFIGS['folder_id']
    mime_type = 'application/vnd.google-apps.spreadsheet'
    drive = GoogleDrive()
    return drive.upload(folder_id, csv_path, mime_type)


def get_new_apps():
    diff_path = os.path.join(os.path.dirname(__file__), 'data/diff.json')
    diff_file = open(diff_path)
    diffs = json.load(diff_file)
    diff_file.close()
    new_apps = [
        app['New'] for app in diffs if app['Old'] == 'None' and app['New']
    ]
    return new_apps


def send_email(file_id, new_apps):
    base_url = 'https://docs.google.com/spreadsheets/d/'
    csv_url = base_url + file_id
    content = 'CSV URL:\t' + csv_url
    content += '\n\nNew Apps:\n'
    for app in new_apps:
        content += '\t\t%s\t\t%s\n' % (app['app name'], app['package name'])
    email.send_email(CONFIGS['mail_host'], CONFIGS['mail_user'],
                     CONFIGS['mail_pwd'], CONFIGS['to_addrs'],
                     'Xiaomi App Store Update', content)


def main():
    new_apps = get_new_apps()
    if not new_apps:
        return
    init_configs()
    xm_gp = get_package_names()
    xm_apps = get_xiaomi_apps()
    print 'Save CSV file.'
    csv_path = gen_csv(xm_apps, xm_gp)
    if not csv_path:
        print 'Save CSV file failed.'
        return
    print 'Upload CSV file.'
    file_id = upload_csv(csv_path)
    if not file_id:
        print 'Upload CSV file failed.'
        return
    send_email(file_id, new_apps)


if __name__ == '__main__':
    main()
