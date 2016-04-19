#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.selector import Selector
import utils


class FuLiDang(Spider):
    name = 'fulidang.com'
    start_urls = ['http://www.fulidang.com/page/1']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('/html/body/section/div/div[@class="content"]/article')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0]
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('span/text()').extract()[0]
                description = utils.join_text(description)
                # image URL
                img = item.xpath('div/a/img/@src').extract()[0]
                # YYYY-MM-DD
                date = item.xpath('p/span[1]/text()').extract()[0]
                date = utils.parse_date(date)
                # label of category
                category = item.xpath('header/a/text()').extract()[0]
            except IndexError:
                continue

        url_prefix, cur_page = response.url.rsplit("/", 1)
        next_page = url_prefix + "/" + str(int(cur_page) + 1)
        yield Request(next_page, self.parse)
