import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["digital"]

mycol = mydb["digital"]



class QuotesSpider(scrapy.Spider):
    name = "digital"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 197):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.thedigitaltransformationpeople.com/supplier_directory/page/{i}/', callback=self.parse_two)
            
    def parse_two(self, response):

        links = response.css('li a.button::attr("href")').extract()

        print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        try:
            firm = response.css('h2::text').extract_first().strip()
       
            url = response.css('a:contains("Website")::attr("href")').extract_first()

            address = response.css('div.address::text').extract_first().strip().replace('\t', '')

            linkedin = response.css('a:contains("LinkedIn")::attr("href")').extract_first()

            sector = response.css('ul.supplier-directory-single__lists > li::text').extract_first()


            details = {'Source': 'https://www.spoke.com/', 'Firm': firm, 'URL': url, 'Linkedin URL': linkedin,
                        'Address Line 1': address, 'Business Sector 1': sector}

            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')

