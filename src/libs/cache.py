#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import wget
import os.path
import subprocess


CACHE_ROOT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '../../cache',
)
if not os.path.exists(CACHE_ROOT):
    os.mkdir(CACHE_ROOT)


def get_cache_url(url):
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(CACHE_ROOT, file_name)
    # file exists, return directly
    if os.path.exists(file_path):
        return os.path.join('/cache', file_name)
    else:
        tmp_path = file_path + '.tmp'
        # delete old one
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        cmd = 'wget {url} -O {tmp_path} -q && mv {tmp_path} {file_path}'.format(
            url=url, tmp_path=tmp_path, file_path=file_path
        )
        subprocess.Popen(cmd, shell=True)
        return url
