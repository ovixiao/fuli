#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import wget
import config
import os.path
import subprocess
from cdn import CDN


_cdn_domain = config.get_config().get('cdn', 'domain')
_cdn = CDN()
CACHE_ROOT = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    '../../cache',
)
if not os.path.exists(CACHE_ROOT):
    os.mkdir(CACHE_ROOT)


def get_cache_url_local(url):
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(CACHE_ROOT, file_name)
    return os.path.join('/cache', file_name)


def get_cache_url_cdn(url):
    file_name = url.rsplit('/', 1)[-1]
    return os.path.join(_cdn_domain, 'cache', file_name)


def get_cache_url(url):
    if url.endswith('.mp4'):
        return get_cache_url_cdn(url)
    else:
        return get_cache_url_local(url)


def cache_remote_cdn(url):
    file_name = url.rsplit('/', 1)[-1]
    cdn_path = os.path.join('cache', file_name)
    if not _cdn.exists(cdn_path):
        return _cdn.upload_remote_image(cdn_path, url)
    else:
        return True


def cache_remote_local(url):
    file_name = url.rsplit('/', 1)[-1]
    file_path = os.path.join(CACHE_ROOT, file_name)
    tmp_path = file_path + '.tmp'
    # delete old one
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    cmd = 'wget {url} -O {tmp_path} -q && mv {tmp_path} {file_path}'.format(
        url=url, tmp_path=tmp_path, file_path=file_path
    )
    subprocess.Popen(cmd, shell=True)


def cache_remote(url):
    if url.endswith('.mp4'):
        cache_remote_cdn(url)
    else:
        cache_remote_local(url)


def cache_local(file_path):
    file_name = file_path.rsplit('/', 1)[-1]
    cdn_path = os.path.join('cache', file_name)
    if not _cdn.exists(cdn_path):
        return _cdn.upload_local_image(cdn_path, file_path)
    else:
        return True


if __name__ == '__main__':
    import sys
    path = sys.argv[1]
    files = os.listdir(path)
    for f in files:
        file_path = os.path.join(path, f)
        cache_local(file_path)
