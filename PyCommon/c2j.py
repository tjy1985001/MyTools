#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import json
import sys


def csv2json(csv_path, json_path):
    csv_file = open(csv_path, 'r')
    json_file = open(json_path, 'w')

    field_names = csv_file.readline().strip().split(',')
    json_data = [row for row in csv.DictReader(csv_file, field_names)]
    json.dump(json_data, json_file, indent=4)
    csv_file.close()
    json_file.close()


if __name__ == '__main__':
    csv2json(sys.argv[1], sys.argv[2])
