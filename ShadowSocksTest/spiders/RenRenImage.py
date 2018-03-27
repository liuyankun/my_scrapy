# -*- coding: UTF-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from ShadowSocksTest.items import ShadowsockstestItem


class RenRenImageSpider(CrawlSpider):

    register = 0
    name = "renrenspider"

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    }


    def start_requests(self):
        return [Request("http://www.renren.com/PLogin.do", meta={'cookiejar': 1}, callback=self.post_login)]


    def post_login(self, response):
        return scrapy.FormRequest.from_response(
            response,
            meta={'cookiejar': response.meta['cookiejar']},
            formdata={'email': '286208654@qq.com', 'password': 'liuyankun1988','autoLogin':'false'},
            callback=self.after_login,
            dont_filter=True
        )

    def after_login(self, response):
        return scrapy.Request("http://photo.renren.com/photo/236973983/albumlist/v7?offset=0&limit=40&showAll=1#"
                              ,callback=self.parse_alums)

    def parse_alums(self, response):
        for album in response.css('.album-list').css('li'):
            url =  album.css('.album-name').css('a::attr(href)').extract_first()
            name =  album.css('.album-name').css('a::text').extract()
            RenRenImageSpider.register = RenRenImageSpider.register+1
            self.logger.info(RenRenImageSpider.register)
            self.logger.info('相册名称:%s',name)
            # self.logger.info(url)
            yield scrapy.Request(url, callback=self.down_pic)
        # next_page = response.css('a[title="下一页"]::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse_alums)

    def down_pic(self,response):
        url = response.url

        for img in response.css('photo-list').css('img'):
            item = ShadowsockstestItem()
            img_url = img.xpath('@src').extract_first()
            yield {'image_urls': [img_url]}
        if next_page is not None:
            yield response.follow(next_page, callback=self.down_pic)