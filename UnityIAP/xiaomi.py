#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import codecs
import threading
from multiprocessing.dummy import Pool as ThreadPool
import requests
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(__file__) + "/..")
import UnityAnalytics.upid as upid

CONFIGS_NAME = 'configs.json'


class XiaomiApps(object):
    app_infos_name = 'apps.json'
    diff_infos_name = 'diff.json'
    download_try_count = 2

    def __init__(self, configs_path):
        self.__lock = threading.Lock()
        self.__local = threading.local()
        self.__old_app_infos = {}
        self.__diff_infos = []

        configs_file = open(configs_path)
        configs = json.load(configs_file)
        configs_file.close()

        self.package_names = configs['package names']
        data_dir = os.path.join(os.path.dirname(__file__), configs['data dir'])
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.__app_infos_path = os.path.join(data_dir, self.app_infos_name)
        self.__diff_infos_path = os.path.join(data_dir, self.diff_infos_name)
        self.__apks_dir = os.path.join(data_dir, 'apks')

    def __get_app_info(self, package_name):
        print 'get app info: ' + package_name
        url = 'http://app.mi.com/details?id=' + package_name
        resp = self.__local.SESSION.get(url=url, allow_redirects=False)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        intro = soup.select('div .intro-titles')[0].contents
        company = intro[0].contents[0]
        app_name = intro[1].contents[0]
        genre = intro[2].contents[1]

        details = soup.select('div .details')[0].contents[0].contents
        app_size = details[1].contents[0]
        current_version = details[3].contents[0]
        update_date = details[5].contents[0]
        app_id = details[9].contents[0]
        return {
            'package name': package_name,
            'app id': app_id,
            'app name': app_name,
            'company': company,
            'genre': genre,
            'current version': current_version,
            'update date': update_date,
            'app size': app_size
        }

    def __download_apk(self, package_name, app_id):
        print 'Download app,', package_name
        url = 'http://app.mi.com/download/' + app_id
        if not os.path.exists(self.__apks_dir):
            os.makedirs(self.__apks_dir)
        apk_path = os.path.join(self.__apks_dir, package_name + '.apk')
        try_count = self.download_try_count
        while try_count > 0:
            try_count -= 1
            try:
                resp = self.__local.SESSION.get(url=url, stream=True)
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

    def __load_app_infos(self):
        if not os.path.exists(self.__app_infos_path):
            return {}
        file_content = open(self.__app_infos_path)
        try:
            app_infos = json.load(file_content)
        except:
            app_infos = {}
        file_content.close()
        return app_infos

    def __save_app_infos(self, app_infos, app_infos_path):
        print 'save app infos:', len(app_infos), app_infos_path
        file_content = codecs.open(app_infos_path, 'w', encoding='utf-8')
        file_content.write(
            json.dumps(
                app_infos, ensure_ascii=False, indent=4, sort_keys=True))
        file_content.close()

    def __arr2dict(self, app_infos, key):
        dic = {}
        for info in app_infos:
            dic[info[key]] = info
        return dic

    def __get_upid(self, app_info):
        apk_path = self.__download_apk(app_info['package name'],
                                       app_info['app id'])
        if not apk_path:
            print 'Download %s failed.' % app_info['package name']
            return None
        ua_info = upid.get_upid(apk_path)
        return ua_info[2] if ua_info[2] else ua_info[3]

    def __update_an_app(self, package_name):
        if not self.__local.__dict__.has_key('SESSION'):
            self.__local.SESSION = requests.session()
        app_info = self.__get_app_info(package_name)
        try:
            self.__lock.acquire()
            old_app_info = self.__old_app_infos[package_name]\
                if self.__old_app_infos.has_key(package_name) else None
            if not app_info:
                self.__diff_infos.append({'Old': old_app_info, 'New': 'None'})
                return
        finally:
            self.__lock.release()
        need_update = True
        if old_app_info:
            app_info['UPID'] = old_app_info['UPID']
            need_update = cmp(old_app_info, app_info) != 0
        if need_update:
            print package_name, 'has update'
            app_info['UPID'] = self.__get_upid(app_info)
            try:
                self.__lock.acquire()
                self.__old_app_infos[package_name] = app_info
                self.__diff_infos.append({
                    'Old': old_app_info,
                    'New': app_info
                })
            finally:
                self.__lock.release()

    def refresh(self):
        pool = ThreadPool()
        self.__old_app_infos = self.__arr2dict(self.__load_app_infos(),
                                               'package name')
        pool.map(self.__update_an_app, self.package_names)
        pool.close()
        pool.join()
        if self.__diff_infos:
            self.__save_app_infos(self.__old_app_infos.values(),
                                  self.__app_infos_path)
            self.__save_app_infos(self.__diff_infos, self.__diff_infos_path)


def main():
    configs_path = os.path.join(os.path.dirname(__file__), CONFIGS_NAME)
    apps = XiaomiApps(configs_path)
    apps.refresh()


if __name__ == '__main__':
    main()
