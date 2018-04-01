# -*- coding: UTF-8 -*-
import scrapy
import scrapy_splash
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest

from ShadowSocksTest.items import ShadowsockstestItem


class RenRenImageSpider(CrawlSpider):

    register = 0
    name = "renrenspider"

    script = """ 
            function main(splash) 
                 local cookies = splash.args.headers['Cookie']
                splash:on_request(
                    function(request)
                        request:set_header('Cookie', cookies)
                    end
                )
                splash:go{splash.args.url, headers=splash.args.headers}
                splash:wait(2)

                local scroll_to = splash:jsfunc("window.scrollTo")
                local get_body_height = splash:jsfunc(
                    "function() {return document.body.scrollHeight;}"
                )
                splash:wait(splash.args.wait)
                for _ = 1, 10 do
                    scroll_to(0, get_body_height())
                    splash:wait(1)
                end 

                splash:wait(2)
                local entries = splash:history()
                local last_response = entries[#entries].response
                return {
                    url = splash.args.url,
                    html = splash:html(),
                    http_status = last_response.status,
                    headers = last_response.headers,
                    cookies = splash:get_cookies(),
                    png = splash:png{width=640},
                    har = splash:har(),
                }
            end 
            """

    script_1 = """ 
            function main(splash) 
                 local cookies = splash.args.headers['Cookie']
                splash:on_request(
                    function(request)
                        request:set_header('Cookie', cookies)
                    end
                )
                splash:go{splash.args.url, headers=splash.args.headers}
                splash:wait(2)

                local scroll_to = splash:jsfunc("window.scrollTo")
                local get_body_height = splash:jsfunc(
                    "function() {return document.body.scrollHeight;}"
                )
                splash:wait(splash.args.wait)
                for _ = 1, 10 do
                    scroll_to(0, get_body_height())
                    splash:wait(0.5)
                end 

                splash:wait(5)
                local entries = splash:history()
                local last_response = entries[#entries].response
                return {
                    url = splash.args.url,
                    html = splash:html(),
                    http_status = last_response.status,
                    headers = last_response.headers,
                    cookies = splash:get_cookies(),
                    png = splash:png{width=640},
                    har = splash:har(),
                }
            end 
                """

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


        return SplashRequest("http://photo.renren.com/photo/236973983/albumlist/v7?offset=0&limit=40&showAll=1#",
                      args={
                          'wait': 0.5,
                          'lua_source':RenRenImageSpider.script
                      },
                      endpoint='execute',
                      slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                      meta={'cookiejar': response.meta['cookiejar']},
                      callback=self.parse_albums,
                      )

    def parse_albums(self, response):
        #self.logger.info(response.body.decode(response.encoding))
        for album in response.css('.album-box'):
            count = album.css('.album-count').css('span::text').extract_first()
            if int(count) < 1 :
                continue
            url =  album.css('.album-name').css('a::attr(href)').extract_first()
            name = album.css('.album-name').css('a::text').extract_first()

            RenRenImageSpider.register = RenRenImageSpider.register+1
            self.logger.info(RenRenImageSpider.register)
            self.logger.info('相册名称:%s',name)
            self.logger.info('照片数量：%s',count)
            self.logger.info('相册链接：%s',url)
            yield SplashRequest(url=url,
                      args={
                          'wait': 0.5,
                          'lua_source':RenRenImageSpider.script_1
                      },
                      endpoint='execute',
                      slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                      meta={'cookiejar': response.meta['cookiejar']},
                      callback=self.parse_album,
                      )

    def parse_album(self,response):
        #self.logger.info(response.body.decode(response.encoding))
        self.logger.info('相册地址：%s',response.url)
        album_name = response.css('#album-name::text').extract_first()
        self.logger.info('相册名称:%s', album_name)
        a =0
        for photo_box in response.css('.photo-box'):
            #photo_number =photo_box.css('img::attr(alt)').extract_first()
            #view_data = photo_box.css('img::attr(data-viewer)').extract_first()
            #self.logger.info(view_data)
            a = a+1

        self.logger.info('照片数量：%s', a)
            # url = response.url+'#photo/236973983/' + photo_number
            # self.logger.info('照片地址：%s', url)
            # yield SplashRequest(url=url,
            #           args={
            #               'wait': 0.5,
            #               'lua_source':RenRenImageSpider.script
            #           },
            #           endpoint='execute',
            #           slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
            #           meta={'cookiejar': response.meta['cookiejar']},
            #           callback=self.down_pic,
            #           )

    def down_pic(self,response):
        item = ShadowsockstestItem()
        self.logger.info(response.body.decode(response.encoding))
        img = response.css('.pop-content-img viewer-img-show')
        img_url = img.xpath('@src').extract_first()
        yield {'image_urls': [img_url]}
