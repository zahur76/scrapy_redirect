import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["around"]

mycol = mydb["around_B"]



class QuotesSpider(scrapy.Spider):
    name = "around"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 107):
            mainlink = f'https://www.arounddeal.com/company-service/jewellery/{i}'
            yield scrapy.Request(url=mainlink, callback=self.parse_four)


    def parse_four(self, response):

        links = response.css('a.link-dark::attr("href")').extract()

        for link in links:    
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two)
    

    def parse_two(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('div.company-info:contains("Website") + div a::attr("href")').extract_first()

            address = response.css('div.company-info:contains("Headquarters") + div a::text').extract_first()

            sector = response.css('div.company-info:contains("Industry") + div a::text').extract_first()

            details = {'Source': 'https://www.arounddeal.com/', 'Firm': firm, 'URL': url, 'Business Sector 1':sector,
                     'Address Line 1': address, }

            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
