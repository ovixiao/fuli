#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import sys
import time
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler


__inited_loggers = {}
__all__ = ['get_logger', 'MultiProcessingTimedRotatingFileHandler']

# the code of output strings. Default is UTF-8
CODE = 'utf-8'
# the path of log dir relative to the path of this file
RELATIVE_PATH = '../log'


class Logger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super(Logger, self).__init__(name, level)

    def _compose_msg(self, *args, **kwargs):
        """Compose pairs in arguments to format as key=value

        Args:
            args: the string log message.
            kwargs: the log messages. it must follow {key: value} format.

        Returns:
            return the msg_list joint by '\t'.
        """
        global CODE

        msg_list = []
        if len(args) > 0:  # some string should log directly.
            msg_list.extend(map(lambda x: str(x), args))

        if len(kwargs) > 0:  # some pairs should log with compose
            for k, v in kwargs.items():
                # encode to code
                k = k.encode(CODE) if isinstance(k, unicode) else str(k)
                v = v.encode(CODE) if isinstance(v, unicode) else str(v)
                msg_list.append('{0}={1}'.format(k, v))

        return '\t'.join(msg_list)

    def debug(self, *args, **kwargs):
        """Log messages in DEBUG level.
        """
        if self.isEnabledFor(logging.DEBUG):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.DEBUG, msg, [])

    def info(self, *args, **kwargs):
        """Log messages in INFO level.
        """
        if self.isEnabledFor(logging.INFO):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.INFO, msg, [])

    def warning(self, *args, **kwargs):
        """Log messages in WARNING level.
        """
        if self.isEnabledFor(logging.WARNING):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.WARNING, msg, [])

    def error(self, *args, **kwargs):
        """Log messages in ERROR level.
        """
        if self.isEnabledFor(logging.ERROR):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.ERROR, msg, [])

    def critical(self, *args, **kwargs):
        """Log messages in CRITICAL level.
        """
        if self.isEnabledFor(logging.CRITICAL):
            msg = self._compose_msg(*args, **kwargs)
            self._log(logging.CRITICAL, msg, [])

    def exc_info(self):
        """Get exception information

        Returns:
            return the exception infomation as format
            `file name`, `line number`, `function`, `message`
        """
        info = sys.exc_info()
        exc_list = list(traceback.extract_tb(info[2]))
        file, lineno, func, msg = exc_list[-1]
        # get exception
        exc = traceback.format_exc().rstrip()
        exc_index = exc.rfind('\n')
        exc = exc[exc_index + 1:]
        return file, lineno, func, msg, exc


class MultiProcessingTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Logger handler suit for multi processing with time rotate
    """

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, timeTuple)
        if not os.path.exists(dfn):
            os.rename(self.baseFilename, dfn)
        if self.backupCount > 0:
            # find the oldest log file and delete it
            for s in self.getFilesToDelete():
                os.remove(s)
        self.mode = 'a'
        self.stream = self._open()
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and \
                not self.utc:
            dstNow = time.localtime(currentTime)[-1]
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                # DST kicks in before next rollover,
                # so we need to deduct an hour
                if not dstNow:
                    newRolloverAt = newRolloverAt - 3600
                # DST bows out before next rollover, so we need to add an hour
                else:
                    newRolloverAt = newRolloverAt + 3600
        self.rolloverAt = newRolloverAt


def __init_logger(logger_name, log_path, logger_level, **kwargs):
    """Initialize logger

    参数:
        logger_name: logger name
        log_path: path of log file
        logger_level: level for logging action.
        file_level: level for log file.
    """
    global __inited_loggers

    # formatter
    fmt = '%(levelname)s %(asctime)s %(filename)s|%(lineno)d\t%(message)s'
    formatter = logging.Formatter(fmt)

    # logger handler
    handler = MultiProcessingTimedRotatingFileHandler(
        log_path,
        when='MIDNIGHT',
        interval=1,
        backupCount=0,
    )

    file_level = kwargs.get('file_level')
    if not file_level:
        file_level = logger_level
    logger = Logger(logger_name, logger_level)

    # handler level
    handler.setLevel(file_level)
    # handler format
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logger_level)

    if logger_name in __inited_loggers:
        del __inited_loggers[logger_name]
    __inited_loggers[logger_name] = logger


def get_logger(name, **kwargs):
    """To get a logger

    Args:
        name: logger name
        file_level: the level for file to write (OPTION)
    """
    global __inited_loggers, RELATIVE_PATH

    # not exists, initialize one
    if name not in __inited_loggers:
        # the root path for storing log files
        log_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            RELATIVE_PATH,
        )
        # is the path exists? or create it
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        # path of log file
        log_path = os.path.join(
            log_dir,
            '{0}.log'.format(name),
        )
        __init_logger(name, log_path, logging.DEBUG)

    return __inited_loggers[name]
