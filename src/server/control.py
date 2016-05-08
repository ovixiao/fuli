#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import sys
import time
import os.path
import subprocess


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def main():
    cmd_list = [
        ['cd', ROOT_DIR],
        ['./fuli_server.py'] + list(sys.argv)[1:],
        ['./watcher.py', '-f', os.path.join(ROOT_DIR, './static')],
    ]

    sub_process_list = []
    for cmd in cmd_list:
        sub_process = subprocess.Popen(cmd)
        sub_process_list.append(sub_process)


if __name__ == '__main__':
    main()
