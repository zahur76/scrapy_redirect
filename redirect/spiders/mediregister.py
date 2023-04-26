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

mydb = myclient["chinamedivice"]

mycol = mydb["chinamedivice"]

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
    name = "chinamedivice"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        

    def start_requests(self):
        for i in range(1, 798): 
            # print(url_)
            yield scrapy.Request(url=f'http://www.chinamedevice.com/suppliers/1/--1--{i}.html', callback=self.parse_two, dont_filter=True)
            
        

    def parse_two(self, response):

        company_links = response.css('a.ul::attr("href")').extract()


        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        print(response.url)
        try:
      
            firm = response.css("h1::text").extract_first()
            
            # phone = response.css('spam.tel::text').extract_first()

            # address_1 =  response.css('span.street-address::text').extract_first()
            
            # state = response.css('span.region::text').extract_first()

            # country = response.css('span.country-name::attr("content")').extract_first()

            # postal_code = response.css('span.postal-code::attr("content")').extract_first() 

            url = response.css('font[color="#FF6600"]::text').extract_first()

            if not url:
                try:
                    url = response.css('td a.orange::attr("href")').extract_first()
                except:
                    url = None
            
            # email = response.css('.vcard a:nth-of-type(2)::text').extract()

            # print(email)

            details = {'Source': 'http://www.chinamedevice.com/', 'Firm': firm, 'URL': url, 'Country': 'China'}


            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(e)
    
    # https://www.medicregister.com/find/Find.asp?SearchTy=Name&cid=-1&SearchSu=&SearchKe=AllKey&SearchLo=ALL&SearchPa=10

       
    
    
   



