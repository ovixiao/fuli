#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from datetime import datetime
from base import BaseSpider
import db


class ZhaiNanBa(BaseSpider):
    name = 'zhainanba'
    ch_name = u'宅男吧'
    start_urls = ['http://zhainanba.net']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('/html/body/section/div/div/article')
        timeline = db.get_collection('timeline')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0]
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('p[3]/text()').extract()[0]
                description = self._join_text(description)
                # image URL
                img = item.xpath('p[2]/a/img/@src').extract()[0]
                # [tag1, tag2, ...]
                tags = item.xpath('p[4]/span[2]/a/text()').extract()
                # YYYY-MM-DD
                date = item.xpath('p[1]/text()').extract()[0]
                date = date.split("(")[1][:-1]
                date = datetime.strptime(date, '%Y-%m-%d')
                # label of category
                category = item.xpath('header/a/text()').extract()[0]
                self.save(title=title, url=url, description=description,
                          img=img, tags=tags, date=date, category=category)
            except IndexError:
                continue

        next_page = selector.xpath(u'/html/body/section/div/div/div/ul/li/a[text()="下一页"]/@href').extract()[0]
        yield Request(response.urljoin(next_page), self.parse)
