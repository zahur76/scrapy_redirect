import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["visualobj"]

mycol = mydb["visualobj"]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "visualobj"

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2,
    #     'CONCURRENT_REQUESTS': 1
    # }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 122):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://visualobjects.com/app-development/industry/financial-services?page={i}', callback=self.parse_two)
            
    def parse_two(self, response):

        elements = response.css('.company-titles').extract()


        for element in elements:
            try:
               
                firm = Selector(text=element).css("span::text").extract_first()
                
              
                url = Selector(text=element).css("div.visit-website-btn a::attr('href')").extract_first()
                

                details = {'Source': 'https://visualobjects.com/', 'Firm': firm, 'URL': url}


                print(details)
                mycol.insert_one(details)


        
            except Exception as e:
                print(e)
