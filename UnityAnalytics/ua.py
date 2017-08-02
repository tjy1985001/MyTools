#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
If Unity Analytics is turned on:
1. [Android]UnityEngine.Analytics.dll or UnityEngine.Cloud.Analytics.dll exists in assets/bin/Data/Managed
   [iOS]Bulk_UnityEngine.Analytics_0.cpp or Bulk_UnityEngine.Cloud.Analytics_0.cpp exists in Classes/Native
'''

import sys
import zipfile
import os

ANALYTICS_DLL_ENGINE = 'assets/bin/Data/Managed/UnityEngine.Analytics.dll'
ANALYTICS_DLL_SDK = 'assets/bin/Data/Managed/UnityEngine.Cloud.Analytics.dll'
ANALYTICS_CPP_ENGINE = 'Classes/Native/Bulk_UnityEngine.Analytics_0.cpp'
ANALYTICS_CPP_SDK = 'Classes/Native/Bulk_UnityEngine.Cloud.Analytics_0.cpp'


def has_analytics_dll(apk):
    '''If Unity Analytics is turned on:
    1. [>=5.2]assets/bin/Data/Managed/UnityEngine.Analytics.dll exists.
    2. [< 5.2]assets/bin/Data/Managed/UnityEngine.Cloud.Analytics.dll exists.
    '''
    zip_apk = zipfile.ZipFile(apk, 'r')
    files = zip_apk.namelist()
    zip_apk.close()
    return ANALYTICS_DLL_ENGINE in files or ANALYTICS_DLL_SDK in files


def check_android(apk):
    return has_analytics_dll(apk)


def has_analytics_cpp(project):
    '''If Unity Analytics is turned on:
    1. [>=5.2]Classes/Native/Bulk_UnityEngine.Analytics_0.cpp exists.
    2. [< 5.2]Classes/Native/Bulk_UnityEngine.Cloud.Analytics_0.cpp exists.
    '''
    engine = os.path.exists(os.path.join(project, ANALYTICS_CPP_ENGINE))
    sdk = os.path.exists(os.path.join(project, ANALYTICS_CPP_SDK))
    return engine or sdk


def check_ios(project):
    return has_analytics_cpp(project)


def main(argv):
    'main function'
    if not argv or len(argv) < 2:
        return
    is_on = False
    if argv[0] == '-ios':
        is_on = check_ios(argv[1])
    elif argv[0] == '-android':
        is_on = check_android(argv[1])
    print 'Unity Analytis is', 'On.' if is_on else 'Off.'


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Exception, ex:
        print ex
