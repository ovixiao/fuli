#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class PageNavi(object):

    def __init__(self, cur_page, max_page, **kwargs):
        """Generate a PageNavi instance.

        Args:
            cur_page: current page number.
            max_page: total pages.
            page_range: range of pages expanded for display, default is 3.
        """
        self._cur_page = cur_page
        self._max_page = max_page
        self._page_range = kwargs.get('page_range', 3)

    @property
    def cur_page(self):
        return self._cur_page

    @property
    def max_page(self):
        return self._max_page

    @property
    def page_range(self):
        return self._page_range

    @property
    def page_list(self):
        if '_page_list' not in dir(self) or not self._page_list:
            page_iter = range(self.cur_page - self.page_range,
                              self.cur_page + self.page_range + 1)
            self._page_list = [x for x in page_iter if 0 < x <= self.max_page]

        return self._page_list

    @property
    def first_page(self):
        return 1

    @property
    def last_page(self):
        return self.max_page

    @property
    def prev_page(self):
        return max(self.first_page, self.cur_page - 1)

    @property
    def next_page(self):
        return min(self.last_page, self.cur_page + 1)


if __name__ == '__main__':
    pagenavi = PageNavi(9, 10)
    print pagenavi.first_page
    print pagenavi.last_page
    print pagenavi.prev_page
    print pagenavi.next_page
    print pagenavi.page_list
