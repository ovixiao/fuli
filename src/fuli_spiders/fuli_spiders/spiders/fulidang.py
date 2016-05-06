#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from base import BaseSpider


class FuLiDang(BaseSpider):
    name = 'fulidang'
    ch_name = u'福利档'
    start_urls = ['http://www.fulidang.com/page/1']
    white_list = set([u'求出处', u'美图集', u'门事件', u'番号档', u'艺人档',
                      u'Rosi', u'Disi', u'Tuigirl', u'Ru1mm'])

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('/html/body/section/div/div[@class="content"]/article')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0]
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('span/text()').extract()[0]
                description = self._join_text(description)
                # image URL
                img = item.xpath('div/a/img/@src').extract()[0]
                # YYYY-MM-DD
                date = item.xpath('p/span[1]/text()').extract()[0]
                date = self._parse_date(date)
                # label of category
                category = item.xpath('header/a/text()').extract()[0]
                if category not in self.__class__.white_list:
                    continue

                self.save(title=title, url=url, description=description,
                          img=img, date=date, category=category)
            except IndexError:
                continue

        url_prefix, cur_page = response.url.rsplit("/", 1)
        next_page = url_prefix + "/" + str(int(cur_page) + 1)
        yield Request(next_page, self.parse)
