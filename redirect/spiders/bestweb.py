import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bestweb"]

mycol = mydb["bestweb"]


class QuotesSpider(scrapy.Spider):
    name = "bestweb"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
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
        for i in range(1, 5945):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.bestwebdesignagencies.co/usa/directory/web-design-companies?page={i}', callback=self.parse_two)
            
    def parse_two(self, response):

        elements = response.css('div.listing').extract()

        for element in elements:
            try:
               
                firm = Selector(text=element).css(".list-title h2 a::text").extract_first()
                
              
                url = Selector(text=element).xpath("//*[@id='sl']/div[1]/div/div[4]/div[2]/div[1]/div[1]/div[2]").extract_first()


                address = Selector(text=element).css("p.location::text").extract_first()
                

                details = {'Source': 'https://www.bestwebdesignagencies.co/', 'Firm': firm, 'URL': url, 'Address Line 1': address, 'Business Sector 1': 'Web Design'}


                print(details)
                # mycol.insert_one(details)

        
            except Exception as e:
                print(e)
