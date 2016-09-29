#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os


def exe_cmd(cmd):
    ret = os.popen(cmd)
    text = ret.read()
    ret.close()
    return text

def get_devices():
    ret = exe_cmd('adb devices')
    lines = ret.split('\n')
    devices = [];
    for i in range(1, len(lines)):
        if len(lines[i]) > 0:
            parts = lines[i].split('\t');
            devices.append(parts[0])
    return devices

def output_devices(devices):
    for device in devices:
        print device

def exe_adb(args, sys_argv):
    cmd = 'adb'
    if args != None and len(args) > 0:
        for arg in args:
            cmd = cmd + ' ' + arg
    
    for i in range(1, len(sys_argv)):
        cmd = cmd + ' ' + sys_argv[i]

    # print cmd
    os.system(cmd)

def main(argv):
    if len(argv) <= 1 : return

    devices = get_devices()
    if len(devices) <= 1:
        exe_adb(None, argv)
        return
    
    output_devices(devices)
    while True:
        tmp = str(input())
        tmp_devices = []
        for device in devices:
            if device.startswith(tmp):
                tmp_devices.append(device)
                break
        
        if len(tmp_devices) > 1:
            output_devices(tmp_devices)
        elif len(tmp_devices) == 1:
            exe_adb(['-s ' + tmp_devices[0]], argv)
            break
        else:
            output_devices(devices)

if __name__ == '__main__':
    try:
        main(sys.argv)
    except:
        pass
    