import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os
import pymongo

# http://www.lacartes.com/business
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["biospace"]

mycol = mydb["biospace"]

company_list = []

company_details = []

count = []

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "biospace"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        

    def start_requests(self):
        for i in range(1, 2036): 
            # print(url_)
            yield scrapy.Request(url=f'https://www.biospace.com/employers/{i}/', callback=self.parse_two, dont_filter=True)
            
        

    def parse_two(self, response):
        print(response.url)
        company_links = response.css('h3.lister__header a::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):

        try:
      
            firm = response.css("h1::text").extract_first()
            
         
            address_1 =  response.css('#address-streetaddress::attr("content")').extract_first()
            
            state = response.css('#address-region::attr("content")').extract_first()

            country = response.css('#address-country::attr("content")').extract_first()

            url = response.css('p.recruiter-website-link a::attr("href")').extract_first()
            

            details = {'Source': 'https://www.biospace.com/', 'Firm': firm, 'URL': url, 'Address Line 1': address_1,
                        'State Or County': state, 'Country': country}


            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(e)
    
    
    

       
    
    
   



