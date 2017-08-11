#!/usr/bin/env python
# -*- coding:utf-8 -*-
'extract UPID from apk'

import sys
import os
import shutil
import re
import zipfile


def get_upid(apk):
    if not apk.endswith('.apk') or not os.path.isfile(apk):
        return (None, None, None, 'invalid input')
    apk_name = os.path.basename(apk)
    tmp_dir = 'temp'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    zip_file = zipfile.ZipFile(apk)
    binary = None
    for tmp in zip_file.namelist():
        if tmp.endswith('globalgamemanagers') or tmp.endswith('mainData'):
            binary = tmp
            seek_index = 20
            read_len = 7
            break
        elif tmp.endswith('data.unity3d'):
            binary = tmp
            seek_index = 18
            read_len = 10
            break
    if not binary:
        return (apk_name, None, None, 'cannot find target binary file')
    binary = zip_file.extract(binary, tmp_dir)
    data = open(binary, 'rb')
    data.seek(seek_index)
    version = data.read(read_len)
    main_version = float(version[0:-4])
    upid = None
    errmsg = None
    if main_version < 5.2:
        errmsg = 'not support'
    else:
        exp = ur'(([0-9a-z]+-){4}[0-9a-z]+)'
        for line in data:
            ret = re.search(exp, line)
            if ret:
                upid = ret.group(0)
                break
    zip_file.close()
    data.close()
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    return (apk_name, version, upid, errmsg)


def get_upids(dir_path):
    if not os.path.isdir(dir_path):
        return None
    return [
        get_upid(apk)
        for apk in [
            os.path.join(dir_path, file_name)
            for file_name in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, file_name)) and
            file_name.endswith('.apk')
        ]
    ]


def output(data):
    if not data:
        return
    if type(data) == tuple:
        data = [data]
    for tmp in data:
        print '%s\t%10s\t%s\t%s' % (tmp[0], tmp[1], tmp[2], tmp[3])


def main(argv):
    'main'
    if not argv:
        return
    path = argv[0]
    if os.path.isdir(path):
        output(get_upids(path))
    elif os.path.isfile(path):
        output(get_upid(path))


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
