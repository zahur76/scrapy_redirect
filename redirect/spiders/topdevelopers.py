import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["topdevelopers"]

mycol = mydb["topdevelopers"]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "topdevelopers"

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
        for i in range(1, 107):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.topdevelopers.co/directory/software-development-companies?page={i}', callback=self.parse_two)
            
    def parse_two(self, response):
        print(response.url)
        elements = response.css("div[itemprop='itemListElement']").extract()
      
        for element in elements:
            try:
               
                firm = Selector(text=element).css("span[itemprop='name']::text").extract_first().strip()
                
              
                url = Selector(text=element).css("a.visit_site::attr('href')").extract_first()


                address = Selector(text=element).css("div.set_country p::text").extract_first()
                

                details = {'Source': 'https://www.topdevelopers.co/', 'Firm': firm, 'URL': url, 'Address Line 1': address, 'Business Sector 1': 'Python Developer'}


                print(details)
                mycol.insert_one(details)

        
            except Exception as e:
                print(e)
