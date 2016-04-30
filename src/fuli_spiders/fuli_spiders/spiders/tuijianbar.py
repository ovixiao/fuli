#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.selector import Selector
from base import BaseSpider


class TuiJianBar(BaseSpider):
    name = 'tuijianbar'
    ch_name = u'福利发源地'
    start_urls = ['http://tuijianbar.com']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('/html/body/section/div/div/article')
        for item in articles:
            try:
                title = item.xpath('header/h2/a/text()').extract()[0].strip()
                # link URL
                url = item.xpath('header/h2/a/@href').extract()[0]
                description = item.xpath('p[3]/text()').extract()[0]
                description = self._join_text(description)
                # image URL
                img = item.xpath('p[2]/a/span/span/img/@data-original').extract()[0]
                tags = item.xpath('p[4]/span[3]/a/text()').extract()
                # YYYY-MM-DD
                date = item.xpath('p[1]/text()').extract()[0]
                date = self._parse_date(date.rsplit(" ", 1)[1])
                # label of category
                category = item.xpath('header/a/text()').extract()[0]
                self.save(title=title, url=url, description=description,
                          img=img, tags=tags, date=date, category=category)
            except IndexError:
                continue

        next_page = selector.xpath('/html/body/section/div/div/div/ul/li[@class="next-page"]/a/@href').extract()[0]
        print next_page
        yield Request(response.urljoin(next_page), self.parse)
