# -*- coding: UTF-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from ShadowSocksTest.items import ShadowsockstestItem


class CroLAXSpider(CrawlSpider):

    register = 0
    name = "crolax"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://3g.renren.com/"
    }


    def start_requests(self):
        return [Request("http://3g.renren.com/login.do?autoLogin=true&&fx=0", meta={'cookiejar': 1}, callback=self.post_login)]


    def post_login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            meta={'cookiejar': response.meta['cookiejar']},
            formdata={'email': '286208654@qq.com', 'password': 'liuyankun1988','remember':'1'},
            callback=self.after_login,
            dont_filter=True
        )

    def after_login(self, response):
        return scrapy.Request("http://3g.renren.com/album/wmyalbum.do?id=236973983&sid=ntYw2JUQ5V9eCGW9yzoZE3&j3fl0z&htf=38&ret=profile.do%3Fid%3D236973983%26htf%3D2-n-%E6%88%91%E7%9A%84%E4%B8%AA%E4%BA%BA%E4%B8%BB%E9%A1%B5-n-0"
                              ,callback=self.parse_alums)

    def parse_alums(self, response):
        for album in response.css('.list').css('tr'):
            url =  album.css('td')[1].css('a::attr(href)').extract_first()
            name =  album.css('td')[1].css('a::text').extract()
            CroLAXSpider.register = CroLAXSpider.register+1
            self.logger.info(CroLAXSpider.register)
            self.logger.info('相册名称:%s',name)
            # self.logger.info(url)
            yield scrapy.Request(url, callback=self.down_pic)
        next_page = response.css('a[title="下一页"]::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_alums)

    def down_pic(self,response):
        name = response.css('.sec')[2].css('b::text').extract()
        self.logger.info(name)
        number = response.css('.sec')[3].css('span::text').extract()
        self.logger.info(number)
        next_page = response.css('a[title="下一页"]::attr(href)').extract_first()
        for img in response.css('.list').css('img'):
            item = ShadowsockstestItem()
            img_url = img.xpath('@src').extract_first()
            yield {'image_urls': [img_url]}
        if next_page is not None:
            yield response.follow(next_page, callback=self.down_pic)