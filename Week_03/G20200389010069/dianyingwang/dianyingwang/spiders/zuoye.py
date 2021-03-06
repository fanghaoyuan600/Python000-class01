# -*- coding: utf-8 -*-
import scrapy
from dianyingwang.items import DianyingwangItem

item =DianyingwangItem()
class ZuoyeSpider(scrapy.Spider):
    name = 'zuoye'
    allowed_domains = ['www.rrys2019.com']
    start_urls = ['http://www.rrys2019.com//']
    #获取“24小时下载热门”栏目的电影相关信息，至少包括排行、电影分级、浏览次数、封面信息。

    def parse(self, response):
        dyw_divs = response.xpath('//div[@class="box clearfix"]/ul/li/a')
        for dyw_div in dyw_divs:
            title = dyw_div.xpath('./text()').extract()
            content_list = dyw_div.xpath("./@herf").extract()
            item = DianyingwangItem(title=title,content=content_list)
            yield scrapy.Request(
                url='http://rrys2019.com/' + str(content_list),
                callback=self.parse_next,
                meta={"item": item}
            )

    def parse_next(self, response):
        item = response.meta['item']
        paiming = response.xpath('//div[@class="box score-box"]/ul/li/p/text()').extract()
        seecount = response.xpath('//div[@class="count f4"]/div/label/text()').extract()
        item['paiming'] = paiming
        item['seecount'] = seecount
        yield item