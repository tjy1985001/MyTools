#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tinify
import sys
import os
import shutil

KEYS = ['']
DIRS = ['drawable-hdpi', 'drawable-xhdpi', 'drawable-xxhdpi']
MAX_COMPRESSION_COUNT = 500
current_key_index = 0


def compress(src, dest):
    try:
        print '-------------------------------------------------'
        print 'compress', src
        source = tinify.from_file(src)
        print 'save to', dest
        source.to_file(dest)
        src_size = float(os.path.getsize(src))
        dest_size = float(os.path.getsize(dest))
        print 'compression ratio: %f' % (dest_size / src_size)
    except tinify.AccountError, e:
        print 'error', e
        global current_key_index
        if tinify.compression_count >= MAX_COMPRESSION_COUNT and init_tiny(current_key_index + 1):
            compress(src, dest)
    except tinify.Error, e:
        print 'error', e


# 检查目标文件夹，如果已经存在则清空，否则创建
def init_dirs(dest_dir):
    if os.path.exists(dest_dir):
        print dest_dir, 'folder exists'
        shutil.rmtree(dest_dir)
        print 'delete folder', dest_dir
    print 'create folder', dest_dir
    os.mkdir(dest_dir)
    for tmp_dir in DIRS:
        path = os.path.join(dest_dir, tmp_dir)
        print 'create folder', path
        os.mkdir(path)


def init_tiny(start):
    global current_key_index

    current_key_index = 0
    for i in range(start, len(KEYS)):
        tinify.key = KEYS[current_key_index]
        if tinify.validate():
            current_key_index = i
            return True
    return False


def main():
    if not init_tiny(0):
        return

    src_root_dir = sys.argv[1]
    dest_root_dir = sys.argv[2]
    # print src_dir, dest_dir
    init_dirs(dest_root_dir)

    for tmp_dir in DIRS:
        src_dir_path = os.path.join(src_root_dir, tmp_dir)
        dest_dir_path = os.path.join(dest_root_dir, tmp_dir)
        images = os.listdir(src_dir_path)
        # print images
        for image in images:
            src_path = os.path.join(src_dir_path, image)
            dest_path = os.path.join(dest_dir_path, image)
            # print src_path, dest_path
            compress(src_path, dest_path)


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        main()
