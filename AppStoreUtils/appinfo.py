#!/usr/bin/env python
# -*- coding:utf-8 -*-
'app info class'

import time
import json


class AppInfo(object):
    'App Info Class'

    def __init__(self, json_data):
        if json_data.has_key('results'):
            result = json_data['results'][0]
            self.version = result['version']
            self.current_version_release_date = self.format_time(
                result['currentVersionReleaseDate'])
            self.bundle_id = result['bundleId']
            self.app_id = result['trackId']
            self.release_date = self.format_time(result['releaseDate'])
            self.app_name = result['trackName']
        else:
            self.version = json_data['version']
            self.current_version_release_date = json_data[
                'current_version_release_date']
            self.bundle_id = json_data['bundle_id']
            self.app_id = json_data['app_id']
            self.release_date = json_data['release_date']
            self.app_name = json_data['app_name']

    def format_time(self, time_str):
        '%Y-%m-%dT%H:%M:%SZ -> %Y-%m-%d %H:%M:%S'
        tmp_time = time.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
        return time.strftime("%Y-%m-%d %H:%M:%S", tmp_time)

    def to_dic(self):
        dic = {}
        dic['app name'] = self.app_name
        dic['app id'] = self.app_id
        dic['bundle id'] = self.bundle_id
        dic['release date'] = self.release_date
        dic['version'] = self.version
        dic['update date'] = self.current_version_release_date
        return dic

    def output_info(self):
        'output detailed info'
        print json.dumps(self.__dict__, indent=4, ensure_ascii=False)
