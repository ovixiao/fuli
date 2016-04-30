#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from datetime import datetime
from base import BaseSpider
import db


class DiaoSiQingNian(BaseSpider):
    name = 'dsqnw'
    ch_name = u'屌丝青年'
    start_urls = ['http://www.dsqnw.com/']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('//article[contains(@class, "type-post")]')
        for item in articles:
            try:
                title = item.xpath('div/div[2]/h2/a/text()').extract()[0]
                # link URL
                url = item.xpath('div/div[2]/h2/a/@href').extract()[0]
                description = item.xpath('div/div[2]/div/div/text()').extract()[0]
                description = self._join_text(description)
                # image URL
                img = item.xpath('div/div[1]/a/img/@src').extract()[0]
                tags = item.xpath('div/div[2]/div/div/div/div[2]/a/text()').extract()
                # YYYY/M/D
                date = item.xpath('div/div[2]/div/div/div/div[3]/a/text()').extract()[0]
                date = datetime.strptime(date, '%Y/%m/%d')
                self.save(title=title, url=url, description=description,
                          img=img, tags=tags, date=date)
            except IndexError:
                continue

        next_page = selector.xpath(u'//div[@class="page-nav"]/a[text()="»"]/@href').extract()[0]
        yield Request(response.urljoin(next_page), self.parse)
