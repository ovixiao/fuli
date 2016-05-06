#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A manage class of CDN based on QiNiu: http://www.qiniu.com
"""
import qiniu
import os
import wget
import config


class CDN(object):

    def __init__(self):
        self.__client = self.__init_client()
        conf = config.get_config()
        self.__bucket_name = conf.get('cdn', 'bucket_name')
        self.__bucket = qiniu.BucketManager(self.__client)

    def __init_client(self):
        conf = config.get_config()
        client = qiniu.Auth(conf.get('cdn', 'access_key'),
                            conf.get('cdn', 'secret_key'))
        return client

    def upload_local_image(self, cdn_path, file_path):
        """Upload local image to CDN

        Args:
            cdn_path: the name of file storing in CDN
            file_path: the path of file for uploading

        Returns:
            return whether it's uploaded.
        """
        token = self.__client.upload_token(self.__bucket_name, cdn_path)
        # convert it into jpeg
        ret, info = qiniu.put_file(token, cdn_path, file_path,
                                   mime_type='image/jpeg', check_crc=True)
        return ret['key'] == cdn_path and ret['hash'] == qiniu.etag(file_path)

    def upload_remote_image(self, cdn_path, url):
        """Upload remote image to CDN.

        Args:
            cdn_path: the name of file storing in CDN
            url: the remote image URL

        Returns:
            return whether it's uploaded.
        """
        file_path = wget.download(url)
        result = self.upload_local_image(cdn_path, file_path)
        os.remove(file_path)
        return result

    def exists(self, cdn_path):
        """Whether is the file exists?

        Args:
            cdn_path: the path of file storing in CDN

        Returns:
            return whether it exits
        """
        ret, info = self.__bucket.stat(self.__bucket_name, cdn_path)
        # exists is not None
        return not(ret is None)
