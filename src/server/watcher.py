#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import time
import argparse
from scss import parser
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class ScssMonitor(object):

    class MonitorHandler(PatternMatchingEventHandler):

        def update_css(self, scss_path):
            # modify the suffix
            css_path = scss_path.rsplit(".", 1)[0] + ".css"
            with open(css_path, 'w') as f:
                p = parser.Stylesheet(options={'compress': True,
                                               'warn': False})
                scss_text = p.load(scss_path)
                f.write(scss_text)

        def on_created(self, event):
            self.update_css(event.src_path)

    def __init__(self, path, patterns=['*.scss']):
        handler = self.MonitorHandler(patterns=patterns)
        self._observer = Observer()
        self._observer.schedule(handler, path)

    def __del__(self):
        try:
            self._observer.stop()
        except:
            pass

    def start(self):
        self._observer.start()
        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()

        self._observer.join()


def main():
    parser = argparse.ArgumentParser(description='download logs')
    parser.add_argument('-f', '--file', action='store', dest='file_path',
                        help='the files you want to watch', default=[])
    args = parser.parse_args()

    scss_monitor = ScssMonitor(args.file_path)
    scss_monitor.start()


if __name__ == '__main__':
    main()
