#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.selector import Selector
from datetime import datetime


class WuXianFuLi(Spider):
    name = 'wuxianfuli.cc'
    start_urls = ['http://wuxianfuli.cc/']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('/html/body/section/div/div/article')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0]
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('p[3]/text()').extract()[0]
                # image URL
                img = item.xpath('p[2]/a/img/@data-original').extract()[0]
                # [tag1, tag2, ...]
                tags = item.xpath('p[4]/span[3]/a/text()').extract()
                # YYYY-MM-DD
                date = item.xpath('p[1]/text()').extract()[0][9:]
                date = datetime.strptime(date, '%Y-%m-%d')
            except IndexError:
                continue

        next_page = selector.xpath(u'/html/body/section/div/div/div/ul/li/a[text()="下一页"]/@href').extract()[0]
        yield Request(response.urljoin(next_page), self.parse)
