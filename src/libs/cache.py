#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import config
from cdn import CDN


_cdn_domain = config.get_config().get('cdn', 'domain')
_cdn = CDN()


def get_cache_url(url):
    file_name = url.rsplit('/', 1)[-1]
    return os.path.join(_cdn_domain, 'cache', file_name)


def cache_remote(url):
    file_name = url.rsplit('/', 1)[-1]
    cdn_path = os.path.join('cache', file_name)
    if not _cdn.exists(cdn_path):
        return _cdn.upload_remote_image(cdn_path, url)
    else:
        return True


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
