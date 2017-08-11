#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import sys
import getopt

WEIGHTS = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
CHECK_CODE = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']


def get_valid_ids(current_id):
    days = [
        time.strftime('%Y%m%d', time.localtime(i))
        for i in range(
            int(
                time.mktime(
                    time.strptime(current_id[6:10] + '0101', '%Y%m%d'))),
            int(
                time.mktime(
                    time.strptime(current_id[6:10] + '1231', '%Y%m%d'))) + 1,
            3600 * 24)
    ]
    ids = [current_id.replace('****', d[4:]) for d in days]
    valid_ids = [
        tmp_id for tmp_id in ids
        if CHECK_CODE[sum([int(x) * y for x, y in zip(tmp_id, WEIGHTS)]) % 11]
        == tmp_id[-1]
    ]
    return valid_ids


def save_ids(ids, save_path):
    if not save_path:
        return
    try:
        ids_file = open(save_path, 'w')
        for tmp_id in ids:
            ids_file.write(tmp_id + '\n')
        ids_file.close()
    except Exception, ex:
        print 'save failed.', save_path, ex


def main(argv):
    'main'
    if not argv:
        return
    opts, args = getopt.getopt(argv, 'i:s:', ['id=', 'save='])
    current_id = save_path = None
    for opt, value in opts:
        if opt == '-i' or opt == '--id':
            current_id = value
        elif opt == '-s' or opt == '--save':
            save_path = value
    valid_ids = get_valid_ids(current_id)
    save_ids(valid_ids, save_path)
    print valid_ids


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
