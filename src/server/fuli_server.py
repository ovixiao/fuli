#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import argparse
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
logger = log.get_logger('fuli')

app = Flask(__name__)


def get_posts(page=1, ln=10):
    """Get posts of tumblr.

    Args:
        page: the page number. default is 1.
        ln: item number per page. default is 10.

    Returns:
        return a generator including the processed post informations.
    """
    page = int(page)
    ln = int(ln)
    # tumblr collection
    tumblr = db.get_collection('tumblr')
    skip = (page - 1) * ln
    items = tumblr.find(
        {'type': 'video', 'video_url': {'$exists': True}},
        projection={'video_url': True, 'thumbnail_url': True,
                    'timestamp': True, 'blog_name': True, 'short_url': True,
                    'duration': True},
        skip=skip, limit=ln, sort=[('date', -1)]
    )
    for item in items:
        dur = item['duration']
        item['duration'] = '{0:02d}:{1:02d}'.format(*divmod(dur, 60))
        item['date'] = utils.pretty_date(item['timestamp'])
        yield item


@app.route('/')
@app.route('/page/<p>')
def page(p=1):
    """Page contents.

    Args:
        p: the page number. default is 1.
    """
    posts = get_posts(p, LN)
    logger.info(uri='page', p=p)
    return render_template('page.html', title=TITLE, description=DESC,
                           cur_page=int(p))


@app.route('/append/<p>')
def append(p):
    """Generate data for appending.

    Args:
        p: the page number.
    """
    posts = get_posts(p, LN)
    logger.info(uri='append', p=p)
    return render_template('append.html', posts=posts)


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
