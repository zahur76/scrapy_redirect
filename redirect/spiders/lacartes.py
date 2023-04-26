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

mydb = myclient["lacartes"]

mycol = mydb["lacartes"]

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
    name = "lacartes"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/lacartes.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 36): 
            # print(url_)
            yield scrapy.Request(url=f'http://www.lacartes.com/search/w/businesses/c/Health/c2/Sports-Medicine/page/{i}', callback=self.parse_two, dont_filter=True)
            
        

    def parse_two(self, response):
        print(response.url)
        company_links = response.css('a.title::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):

        try:
            url = None
            phone = None
            try:
                firm = response.css("div.page-title-inset h1::text").extract_first()
            except Exception as e:
                print(e)
                firm = None

            try:
                contacts = response.css("div.f::text").extract()            
            except Exception as e:
                print(e)
                contacts = None
            if contacts:
                for contact in contacts:
                    if 'http' in contact:
                        url = contact.strip()
                    elif '+' in contact:
                        phone = contact
         
            address =  response.css('div.r div.f div::text').extract()
            
            print(address)
            

            details = {'Source': 'https://www.lacartes.com/', 'Firm': firm, 'URL': url, 'Phone Number': phone, 'Address Line 1': address,
                        'Business Sector 1': 'Sports Medicine/'}


            print(details)
            mycol.insert_one(details)  

        except Exception as e:
            print(e)
    
    
    

       
    
    
   



