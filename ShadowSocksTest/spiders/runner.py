from threading import Thread

from scrapy.crawler import CrawlerRunner, CrawlerProcess
from twisted.internet import reactor

from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from ShadowSocksTest.spiders.RenRenImage import RenRenImageSpider

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

# sttings = get_project_settings()
# runner = CrawlerRunner(sttings)
# d = runner.crawl(RenRenImageSpider)
# d.addBoth(lambda _: reactor.stop())
# reactor.run()

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('renrenspider', domain='renren.com')
#process.crawl('crolax', domain='renren.com')
process.start()
#Thread(target=process.start).start()

# process.start() # the script will block here until the crawling is finished
# crawler.join()