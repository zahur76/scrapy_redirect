import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["manifest"]

mycol = mydb["manifest"]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "manifest"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 254):
            print(f'page: {167}')
            yield scrapy.Request(url=f'https://themanifest.com/corporate-training/companies?page={i}', callback=self.parse_two)
            
    def parse_two(self, response):

        elements = response.css('li.provider-card:nth-of-type(n+3)').extract()

        for element in elements:
            try:
                try:
                    firm = Selector(text=element).css(".provider-header__title a::text").extract_first().strip()
                except Exception as e:
                    print(e)
                    firm = None
                try:
                    url = Selector(text=element).css("a.track-website-visit::attr('href')").extract_first()
                except Exception as e:
                    print(e)
                    url = None
                
                size = Selector(text=element).css("div.employees + span::text").extract_first()

                address = Selector(text=element).css("span.locality::text").extract_first()

                sector = Selector(text=element).css("li.provider-card__industries-item::attr('data-content')").extract_first()
                

                details = {'Source': 'https://themanifest.com/', 'Firm': firm, 'URL': url, 'Company Size: size': size,
                           'Business Sector 1': sector, 'Business Sector 2': 'Corporate Training',
                           'Country': address}


                print(details)
                mycol.insert_one(details)
        
            except Exception as e:
                print(e)
        

        
    