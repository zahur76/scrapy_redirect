import scrapy
from scrapy import signals
from scrapy.selector import Selector
from redirect.spiders.test import converter

import pandas as pd
import js2py
import html
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["yellowA"]

mycol = mydb["yellowA"]


class QuotesSpider(scrapy.Spider):
    name = "yellow"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        

    def start_requests(self):        
        yield scrapy.Request(url=f'https://yellow.place/en/search?q=&country_slug=southafrica', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("a.none::attr('href')").extract()
        

        print(len(company_links))
        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_four , dont_filter=True)

        next_ = response.css('a.js_next_page::attr("href")').extract_first()

        print(next_)

        if next_:
            yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_two)


    def parse_four(self, response):
        # print(response.url)

        try:

            firm =  response.css("h1::text").extract_first()

            print(firm)

            # url = response.css(".i-external a::attr('href')").extract_first()    

            # address = response.css("p span.i-marker::text").extract_first()

            # phone = response.css(".i-call a::attr('href')").extract_first()

            # if address:
            #     address = address.strip()            

            # details = {'Source': 'https://yellow.place/', 'Firm': firm, 'URL': url,'Address Line 1': address, 'Country' : 'South Africa', 'Phone': phone}

            # print(details)

      
            # mycol.insert_one(details)
        
        except Exception as e:
            print(e)
        
        return  
    
   



