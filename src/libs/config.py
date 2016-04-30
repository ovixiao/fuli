#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import ConfigParser
import os


__all__ = ['get_config']
__config = None


def get_config(**kwargs):
    """Get a config instance.

    Args:
        config_file: config file. default is server.cfg

    Returns:
        return a ConfigParser object.
    """
    global __config

    if __config is None:
        config = ConfigParser.ConfigParser()
        # the path is `conf` dir under root dir.
        config_file = kwargs.get('config_file', 'server.cfg')
        config_file = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '../../conf',
            config_file,
        )
        config.read(config_file)

    return config
