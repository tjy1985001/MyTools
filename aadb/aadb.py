#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
When multiple Android devices are connected to computer,
you must execute 'adb devices' to get device serial numbers and use '-s' to specify a device.
aadb could list all connected Android device serial numbers.
You just need to input a prefix of any serial number and press enter key.
'''

import sys
import os

WHILE_LIST_ARGS = [
    'devices', 'start-server', 'kill-server', 'version', 'help', '-h'
]  #some args don't work on specific device, execute cmd directly.


def exe_cmd(cmd):
    'execute a cmd'
    ret = os.popen(cmd)
    text = ret.read()
    ret.close()
    return text


def get_devices():
    'get all connected devices'
    lines = exe_cmd('adb devices').split('\n')
    devices = []
    for line in lines[1:]:
        if line:
            devices.append(line.split('\t')[0])
    return devices


def output_devices(devices):
    'output all connected devices'
    for device in devices:
        print device


def exe_adb(args, sys_argv):
    'execute adb cmd'
    cmd = ''
    if args:
        cmd += ' '.join(args)
    if sys_argv:
        cmd += ' ' + ' '.join(sys_argv)
    cmd = 'adb ' + cmd
    # print cmd
    os.system(cmd)


def main(argv):
    'main function'
    if not argv:
        return

    devices = get_devices()
    if len(devices) <= 1 or argv[0] in WHILE_LIST_ARGS:
        exe_adb(None, argv)
        return

    output_devices(devices)
    while True:
        prefix = raw_input()
        tmp_devices = [
            device for device in devices if device.startswith(prefix)
        ]
        device_num = len(tmp_devices)

        if device_num == 1:
            exe_adb(['-s ' + tmp_devices[0]], argv)
            break
        else:
            output_devices(devices)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
