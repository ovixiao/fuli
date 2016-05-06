#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Spider
from datetime import datetime, timedelta
from pymongo.errors import DuplicateKeyError
import os
import sys
import md5


def add_python_path(path):
    lib_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
    if lib_path != sys.path[0]:
        sys.path.insert(0, lib_path)


# lib of fuli spider
add_python_path('../../../libs')
import db
import cdn

class BaseSpider(Spider):

    exist_count = 0
    img_store = cdn.CDN()

    @staticmethod
    def _parse_date(date):
        ret_date = None
        if u'小时前' in date:  # 22小时前
            hours = int(date.split(u'小时前', 1)[0])
            now = datetime.now() - timedelta(hours=hours)
            ret_date = datetime(now.year, now.month, now.day, now.hour)
        elif u'天前' in date:  # 4天前
            days = int(date.split(u'天前', 1)[0])
            now = datetime.now() - timedelta(days=days)
            ret_date = datetime(now.year, now.month, now.day)
        elif u'周前' in date or u'个月前' in date:  # 4个月前 (12-06)
            date_str = date.split("(", 1)[1][:-1]
            month, day = date_str.split("-")
            month = int(month)
            day = int(day)
            now = datetime.now()
            ret_date = datetime(now.year, month, day)
            if ret_date > now:
                ret_date = datetime(ret_date.year - 1,
                                    ret_date.month, ret_date.day)
        elif u'年前' in date:  # 2年前 (2013-12-29)
            date_str = date.split("(", 1)[1][:-1]
            year, month, day = date_str.split("-")
            year = int(year)
            month = int(month)
            day = int(day)
            ret_date = datetime(year, month, day)

        return ret_date

    @staticmethod
    def _join_text(text):
        text_splited = text.split(u'\n')
        return u''.join([x.strip() for x in text_splited])

    def save(self, **kwargs):
        if self.__class__.exist_count > 10:
            raise RuntimeError('Exceed maximum retry times for database')

        try:
            # add source and chinese source
            kwargs['src'] = self.__class__.name
            kwargs['ch_src'] = self.__class__.ch_name

            # make cdn path
            img_url = kwargs['img'].encode("utf-8")
            cdn_path = md5.new(img_url).hexdigest()
            kwargs['cdn_path'] = cdn_path.decode("utf-8")

            # insert into database
            timeline = db.get_collection('timeline')
            timeline.insert(kwargs)

            # actually upload image here
            if not self.__class__.img_store.exists(cdn_path):
                self.__class__.img_store.upload_remote_image(cdn_path, img_url)

        except DuplicateKeyError:
            self.__class__.exist_count += 1
