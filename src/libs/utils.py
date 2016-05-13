#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from datetime import datetime


def pretty_date(ts):
    """Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    diff = datetime.now() - datetime.fromtimestamp(ts)
    dis = diff.seconds
    did = diff.days

    if did == 0:
        if dis < 10:
            return u"刚刚"
        elif dis < 60:
            return u"{:d} 秒前".format(dis)
        if dis < 3600:
            return u"{:d} 分种前".format(dis / 60)
        elif dis < 86400:
            return u"{:d} 小时前".format(dis / 3600)
    elif did == 1:
        return u"昨天"
    elif did < 7:
        return u"{:d} 天前".format(did)
    elif did < 31:
        return u"{:d} 周前".format(did / 7)
    elif did < 365:
        return u"{:d} 月前".format(did / 30)
    else:
        return u"{:d} 年前".format(did / 365)
