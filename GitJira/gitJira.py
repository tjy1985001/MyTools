#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os, re, sys

BASE_URL = 'http://jira.example.com/browse/' #jira base url
ISSUES_RE = '(EA|EGB)(-|－)([\d]+)'

def exeCmd(cmd):
    ret = os.popen(cmd)
    text = ret.read()
    ret.close()
    return text

def main(argv):
    # print argv
    if len(argv) != 3:
        return
    repos_path = argv[1]
    commit = argv[2]
    os.chdir(repos_path)
    ret = exeCmd('git show ' + commit)
    ret = ret[0:ret.find('diff --git')]
    # print ret
    issues = re.findall(ISSUES_RE, ret, re.I)
    # print issues
    for issue_type, sep, issue_num in issues:
        # print issue_type, issue_num
        exeCmd('open ' + BASE_URL + issue_type + '-' + issue_num)

def test(argv):
    if len(argv) != 3:
        return
    repos_path = argv[1]
    commit = argv[2]
    os.chdir(repos_path)
    ret = exeCmd('git show ' + commit)
    ret = ret[0:ret.find('diff --git')]
    print ret

if __name__ == '__main__':
    main(sys.argv)
    