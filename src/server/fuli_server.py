#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import json
import math
import pymongo
import argparse
from bson.objectid import ObjectId
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
import utils


app = Flask(__name__)


def get_posts(page=1, ln=10):
    tumblr = db.get_collection('tumblr')
    skip = (page - 1) * ln
    items = tumblr.find(
        {'type': 'video', 'video_url': {'$exists': True}},
        projection={'player': False},
        skip=skip, limit=ln, sort=[('date', -1)]
    )
    ret_items = []
    for item in items:
        dur = item['duration']
        item['duration'] = '{:02d}:{:02d}'.format(dur / 60, dur % 60)
        item['date'] = utils.pretty_date(item['timestamp'])
        ret_items.append(item)

    return ret_items


@app.route('/')
@app.route('/page/<p>')
def page(p=1):
    p = int(p)
    ln = 10
    page_navi = PageNavi(page, 785 / ln)
    navi_items = gen_navi_items()
    posts = get_posts(p, ln)
    return render_template(
        'page.html',
        title=u"福利聚合",
        description=u"宅男爱美女",
        cur_page=p,
    )


@app.route('/append/<p>')
def append(p):
    p = int(p)
    ln = 10
    posts = get_posts(p, ln)
    return render_template(
        'append.html',
        posts=posts,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download logs')
    parser.add_argument('--debug', action='store_true', dest='debug',
                        help='Start server in debug mode', default=False)
    args = parser.parse_args()

    app.run(debug=args.debug, port=8888)
