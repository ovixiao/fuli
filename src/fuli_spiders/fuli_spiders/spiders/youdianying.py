#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from scrapy import Request
from scrapy.selector import Selector
from datetime import datetime
from base import BaseSpider
import db


class YouDianYin(BaseSpider):
    name = 'youdianying'
    ch_name = u'有点硬'
    start_urls = ['https://youdian.in/']

    def parse(self, response):
        selector = Selector(response=response)
        articles = selector.xpath('//*[@id="main"]/*/div[@class="post-box"]')
        timeline = db.get_collection('timeline')
        for item in articles:
            try:
                title = item.xpath('div[@class="post-header"]/p/a/text()').extract()[0]
                # link URL
                url = item.xpath('div[@class="post-header"]/p/a/@href').extract()[0]
                description = item.xpath('*/div[@class="post-expert"]/text()').extract()[0]
                description = self._join_text(description)
                # image URL
                img = item.xpath('*/div[@class="post-info"]/a/img/@data-original').extract()[0]
                # YYYY-MM-DD
                #date = item.xpath('*/div[@class="post-date"]/text()').extract()[0].strip()
                date = item.xpath('div[@class="post-content"]/div[@class="post-footer"]/div[@class="post-date"]/text()').extract()[0]
                date = datetime.strptime(date, '%Y-%m-%d')
                self.save(title=title, url=url, description=description,
                          img=img, date=date)
            except IndexError:
                continue

        next_page = selector.xpath(u'//*/div[@class="page-navigator"]/li/a[text()="下一页 »"]/@href').extract()[0]
        yield Request(response.urljoin(next_page), self.parse)
