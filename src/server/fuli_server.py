#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import json
import math
import pymongo
import argparse
from flask import Flask, request
from flask import render_template


def add_python_path(path):
    lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
    if lib_path != sys.path[0]:
        sys.path.insert(0, lib_path)


add_python_path('../libs')
import db
import config
import log
from pagenavi import PageNavi


app = Flask(__name__)


def gen_posts(page):
    ln = 10
    conf = config.get_config()
    cdn_domain = conf.get('cdn', 'domain')
    try:
        page = int(page)
    except ValueError:
        page = 1

    timeline = db.get_collection('timeline')
    db_items = timeline.find(
        skip=(page - 1) * ln,
        limit=ln,
        sort=[('date', pymongo.DESCENDING)],
    )
    items = []
    for item in db_items:
        try:
            item['date'] = str(item['date'].strftime('%Y-%m-%d'))
        except:
            pass
        item['_id'] = str(item['_id'])
        if len(item['description']) > 120:
            item['description'] = item['description'][:120] + '...'
        item['cdn_path'] = os.path.join(cdn_domain, item['cdn_path'])
        items.append(item)
    return items


def gen_navi_items():
    navi_items = [
        {'name': u'福利', 'url': '#'},
        {'name': u'tumblr', 'url': '#'},
        {'name': u'买家秀', 'url': '#'},
    ]
    return navi_items


@app.route('/')
def index():
    page = 1
    page_navi = PageNavi(1, 10)
    navi_items = gen_navi_items()
    posts = gen_posts(page)
    return render_template(
        'index.html',
        navi_items=navi_items,
        posts=posts,
        page_navi=page_navi,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download logs')
    parser.add_argument('--debug', action='store_true', dest='debug',
                        help='Start server in debug mode', default=False)
    args = parser.parse_args()

    app.run(debug=args.debug, port=8888)
