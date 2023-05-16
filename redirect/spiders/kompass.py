import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["kompass"]

mycol = mydb["kompass"]



class QuotesSpider(scrapy.Spider):
    name = "kompass"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 41):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://us.kompass.com/a/business-management-consultants/80300/page-{i}/', callback=self.parse_two)
            
    def parse_two(self, response):

        elements = response.css('.resultatDivId div.prod_list').extract()

        for element in elements:
            try:
                try:
                    firm = Selector(text=element).css("span.titleSpan::text").extract_first().strip()
                except Exception as e:
                    print(e)
                    firm = None
                try:
                    url = Selector(text=element).css("div.companyWeb a::attr('href')").extract_first()
                except Exception as e:
                    print(e)
                    url = None
                

                address = Selector(text=element).css("span.placeText::text").extract_first()

                sector = Selector(text=element).css("p.product-summary span::text").extract_first()

                phone = Selector(text=element).css("div.collapse.freePhone + input::attr('value')").extract_first()
                

                details = {'Source': 'https://themanifest.com/', 'Firm': firm, 'URL': url,
                           'Business Sector 1': sector,
                           'Country': address, 'Telephone Number': phone}


                print(details)
                mycol.insert_one(details)
        
            except Exception as e:
                print(e)
        

        
    