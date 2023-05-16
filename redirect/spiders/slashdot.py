import scrapy
from scrapy import signals
from scrapy.selector import Selector


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["slashdot"]

mycol = mydb["slashdot"]


class QuotesSpider(scrapy.Spider):
    name = "slashdot"
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS': 1
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 1000):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://slashdot.org/software/?regions=mexico&page={i}', callback=self.parse_two)
            
    def parse_two(self, response):

        links = response.css('a.see-project::attr("href")').extract()


        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)

        
    def parse_three(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('div.url div.field-value::text').extract_first()

            address = response.css('div:contains("Headquarters:") + div::text').extract_first()

            details = {'Source': 'https://slashdot.org/', 'Firm': firm, 'URL': url, 'Address Line 1':address}

            print(details)
            # mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')

