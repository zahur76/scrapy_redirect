import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["usinfo"]

mycol = mydb["usinfo"]


company_list = []

company_details = []

links = [
    'https://www.hotfrog.com/search/us/baby-stores'
]


class QuotesSpider(scrapy.Spider):
    name = "usinfo"

    custom_settings = {
        'DOWNLOAD_DELAY': 30,
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
        for i in range(1,51):    
            yield scrapy.Request(url=f'https://www.us-info.com/en/usa/business/31200/entertainment_arts_equipment_rentals/{i}', callback=self.parse_two)


    def parse_two(self, response):
        
        links = response.css('.customer-item-name a::attr("href")').extract()

        print(len(links))
        # for link in links:          
        #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'page': response.url})


    def parse_three(self, response):

        # print(response.url) 
        try:
            firm = response.css('h1.business-name--verified::text').extract_first()

            phone = response.css('dt:contains("Telefoon") + dd::text').extract_first()

            if phone:
                phone = phone.strip()

            url = response.css('dt:contains("Website") + .col-8 a::attr("href")').extract_first()

            address = response.css('dt:contains("Adres") + dd span').extract_first()

            details = {'Source': 'https://www.hotfrog.com/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                        'Address Line 1': address, 'Business Sector': 'Baby Stores'}

            print(details)
            

        except Exception as e:
            print(f'{e}')
