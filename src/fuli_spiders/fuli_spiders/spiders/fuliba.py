#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from datetime import datetime
from base import BaseSpider


class FuLiBa(BaseSpider):
    name = 'fuliba'
    ch_name = u'福利吧'
    start_urls = ['http://fuliba.net']

    def parse(self, response):
        response.replace(body=response.body.replace("<!--", "").replace("-->", ""))
        selector = Selector(response=response)
        articles = selector.xpath('//*[@id="content"]/article')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0].strip()
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('div/p/text()').extract()[1]
                description = self._join_text(description)
                # image URL
                img = item.xpath('div/p/a/img/@src').extract()[0]
                # YYYY-MM-DD
                date = item.xpath('address/text()').extract()[0]
                date = date.split("(")[1][:-1]
                date = datetime.strptime(date, '%Y-%m-%d %H:%M')
                # label of category
                category = item.xpath('header/div[1]/div[1]/a/text()').extract()[0]
                self.save(title=title, url=url, description=description,
                          img=img, date=date, category=category)
            except IndexError:
                continue

        next_page = selector.xpath(u'//*[@id="content-page"]/a[text()="下一页"]/@href').extract()[0]
        yield Request(response.urljoin(next_page), self.parse)
