#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import db
import log
import time
import pymongo
import pytumblr
from math import ceil
from datetime import datetime


class BreakThroughExce(Exception):
    pass


class Tumblr(object):

    INIT_DATE = datetime(1900, 1, 1)

    def __init__(self):
        self._client = pytumblr.TumblrRestClient(
            'V43MvDlU6js2yw0EcRZNUKeagrI7YOvgl68wb45NVSnXR0aARV',
            'Dt4QitP3Hj4jTZnQmMpKT3cIytInZMjhSbh0NVws7X1CtXJYAv',
            'GRkCbNKFZJXmfpMAIdcH1Lu18qUmdtN5ktLLtZ6YApwXnPj6rl',
            'PhOvmPxBrYwVXvgFaDDdjJ5mtYWhqtHph2MnY7iplF9YcrUqnT'
        )
        self._init_db()
        self._logger = log.get_logger('update')

    def _init_db(self):
        self._tumblr = db.get_collection('tumblr')
        self._users = db.get_collection('tumblr_users')

        # tumblr collection
        # store tumblr posts
        self._tumblr.create_index(
            [('id', pymongo.DESCENDING)], unique=True
        )
        self._tumblr.create_index(
            [('date', pymongo.DESCENDING), ('type', pymongo.ASCENDING)],
            unique=True
        )

        # tumbler users collections
        # store tumblr users account
        self._users.create_index(
            [('user', pymongo.ASCENDING)], unique=True
        )
        self._users.create_index(
            [('latest_update_date', pymongo.ASCENDING)]
        )

    def add_users(self, *users):
        for user in users:
            try:
                user = user.split(".", 1)[0]
                self._users.insert({
                    'user': user,
                    'latest_update_date': self.__class__.INIT_DATE,
                })
            except pymongo.errors.DuplicateKeyError:
                continue

    def get_users(self, limit=0, skip=0, **conditions):
        return self._users.find(conditions, skip=skip, limit=limit)

    def update_user(self, item):
        item['latest_update_date'] = datetime.now()
        return self._users.save(item)

    def get_posts(self, user):
        # get the total posts
        info = self._client.blog_info(user)
        total = info['blog']['posts']
        limit = 20  # 20 posts per request
        now = int(time.time())
        try:
            for i in xrange(int(ceil(total / float(limit)))):
                offset = i * limit
                posts = self._client.posts(user, limit=limit, offset=offset)
                for post in posts['posts']:
                    try:
                        # ignore those that later than 30 minutes
                        if now - post['timestamp'] > 1800:
                            raise BreakThroughExce()


                        self._tumblr.insert(post)
                    except pymongo.errors.DuplicateKeyError:
                        continue
                    else:
                        self._logger.info(
                            'add_post', user=user, url=post['post_url'],
                            type=post['type'],
                        )
        except BreakThroughExce:
            pass

    def update(self):
        users = self.get_users()
        self._logger.info('start_update')
        for user_info in users:
            user = user_info['user']
            self._logger.info('update_user', user=user)
            self.get_posts(user)
            self.update_user(user_info)


if __name__ == '__main__':
    tumblr = Tumblr()
    tumblr.update()
