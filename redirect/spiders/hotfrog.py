import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["hotfrog"]

mycol = mydb["hotfrog_global_B"]


class QuotesSpider(scrapy.Spider):
    name = "frog_v2"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    
    def start_requests(self):
       
        for i in range(1, 844):     
            yield scrapy.Request(url=f'https://www.hotfrog.co.uk/search/gb/pest-control/{i}', callback=self.parse_two)



    def parse_two(self, response):
        print(response.url)
        links = response.css('a[data-yext-click=name]::attr("href")').extract()
        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'page': response.url})


    def parse_three(self, response):

        # print(response.url) 
        try:
            firm = response.css('strong.lead::text').extract_first()

            phone = response.css('dt:contains("Phone") + dd::text').extract_first()

            if phone:
                phone = phone.strip()

            url = response.css('dt:contains("Website") + .col-8 a::attr("href")').extract_first()

            state = response.css('span[data-address-county]::text').extract_first()

            city = response.css('span[data-address-town]::text').extract_first()

            postcode = response.css('span[data-address-postcode]::text').extract_first()

            details = {'Source': 'https://www.hotfrog.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                        'State Or County': state, 'City': city, 'Postal Code': postcode, 'Business Sector 1': 'Pest Control'}

            print(details)
   

            mycol.insert_one(details)          



        except Exception as e:
            print(f'{e}')


# https://www.hotfrog.co.uk/search/gb/batteries-%26-power-supply
# https://www.hotfrog.co.uk/search/gb/design-%26-printing
# https://www.hotfrog.co.uk/search/gb/telephone-equipment
