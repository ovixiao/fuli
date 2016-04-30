#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import pymongo
import config


__db = None
__all__ = ['get_collection']


class DB(object):

    def __init__(self):
        self._db = self._init_db()

    def _init_db(self):
        conf = config.get_config()
        client = pymongo.MongoClient(
            conf.get('database', 'host'),
            conf.getint('database', 'port'),
        )
        return client[conf.get('database', 'name')]

    def _init_index(self):
        self._db.timeline.create_index([('date', pymongo.DESCEND)])

    def __getattr__(self, name):
        return self._db.__getattr__(name)


def __init_db():
    global __db

    if __db is None:
        __db = DB()

    return __db


def get_collection(name):
    global __db

    return __db.__getattr__(name)

__init_db()
