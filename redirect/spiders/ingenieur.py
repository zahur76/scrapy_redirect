import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["engineer"]

mycol = mydb["engineer"]


class QuotesSpider(scrapy.Spider):
    name = "engineer"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    
    def start_requests(self):
        for i in range(1, 231):          
            yield scrapy.Request(url=f'https://ingenieursbureaus.nu/zoek?open-day=friday&distance=5&require-website=1&page={i}', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('h4 a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):   
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a[title="Website"]::text').extract_first()

            address = response.css('span[itemprop="streetAddress"]::text').extract_first()

            city = response.css('span[itemprop="addressLocality"]::text').extract_first()

            details = {'Source': 'https://ingenieursbureaus.nu/', 'Firm': firm.strip(), 'URL': url.strip(),
                     'Address Line 1': address.strip(), 'City': city.strip()}

            print(details)

            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
