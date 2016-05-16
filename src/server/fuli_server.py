#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re
import sys
import copy
import argparse
import ujson as json
from base64 import b64encode, b64decode
from flask import Flask, request
from flask import render_template


def add_python_path(path):
    """Add `libs` path to PYTHONPATH
    """
    lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
    if lib_path != sys.path[0]:
        sys.path.insert(0, lib_path)


add_python_path('../libs')
import db
import log
import utils

TITLE = u'福利聚合'
DESC = u'各种福利滑滑就有'
LN = 5
RE_GIF = re.compile('.+\.gif$')
logger = log.get_logger('fuli')

app = Flask(__name__)


def get_posts(page=1, ln=10, t='gif'):
    """Get posts of tumblr.

    Args:
        page: the page number. default is 1.
        ln: the item number per page. default is 10.
        t: the type of posts. default is `video`.

    Returns:
        return a generator including the processed post informations.
    """
    page = int(page)
    ln = int(ln)
    tumblr = db.get_collection('tumblr')
    skip = (page - 1) * ln
    posts = []
    if t == 'video':
        items = tumblr.find(
            {'type': 'video', 'video_url': {'$exists': True}},
            projection={'video_url': True, 'thumbnail_url': True,
                        'timestamp': True, 'summary': True},
            skip=skip, limit=ln, sort=[('date', -1)]
        )
        for item in items:
            if len(item['summary']) == 0:
                del item['summary']
            item['date'] = utils.pretty_date(item['timestamp'])
            item['src_tag'] = b64encode(item['video_url'])
            posts.append(item)
    elif t == 'gif':
        items = tumblr.find(
            {'type': 'photo', 'photos.original_size.url': RE_GIF},
            projection={'photos': True, 'timestamp': True, 'summary': True},
            skip=skip, limit=ln, sort=[('date', -1)]
        )
        for item in items:
            item['date'] = utils.pretty_date(item['timestamp'])
            photos = item['photos']
            del item['photos']
            for photo in photos:
                if not photo['original_size']['url'].endswith('.gif'):
                    continue
                if len(item['summary']) == 0:
                    del item['summary']
                item['ori_size'] = photo['original_size']
                item['alt_size'] = photo['alt_sizes'][2]
                posts.append(item)
                break
    return posts


@app.route('/')
@app.route('/page')
@app.route('/page/<t>')
@app.route('/page/<t>/<p>')
def page(t='gif', p=1):
    """Page contents.

    Args:
        t: the type of content. default is `gif`
        p: the page number. default is 1.
    """
    logger.info(uri='page', p=p, t=t)
    # all other invalid types are `gif`
    if t != 'video':
        t = 'gif'
    return render_template('page.html', title=TITLE, description=DESC,
                           cur_page=int(p), type=t)


@app.route('/append/<t>/<p>')
def append(t='gif', p=1):
    """Generate posts for appending.

    Args:
        t: the type of content. default is `gif`
        p: the page number. default is 1.
    """
    posts = get_posts(p, LN, t)
    logger.info(uri='append', p=p, t=t)
    embed_code = render_template('append.html', posts=posts, type=t)
    return json.dumps({'more': len(posts) == LN,
                       'embed_code': embed_code,
                       'len': len(posts)})


@app.route('/player/<tag>')
def player(tag):
    """The page of player

    Args:
        tag: the b64encoded URL
    """
    url = b64decode(tag)
    return render_template('player.html', url=url, title=TITLE)


def main():
    """Command line.
    """
    parser = argparse.ArgumentParser(description='download logs')
    # debug model
    parser.add_argument('--debug', action='store_true', dest='debug',
                        help='Start server in DEBUG mode', default=False)
    args = parser.parse_args()

    app.run(debug=args.debug, port=8691)


if __name__ == '__main__':
    main()
