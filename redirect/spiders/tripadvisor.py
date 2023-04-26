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

mydb = myclient["tripadvisor"]

mycol = mydb["tripadvisor"]


class QuotesSpider(scrapy.Spider):
    name = "tripadvisor"

    custom_settings = {
        'DOWNLOAD_DELAY': 5,
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
        yield scrapy.Request(url=f'https://www.tripadvisor.com/Restaurants-g186338-London_England.html', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("a.Lwqic::attr('href')").extract()
        
        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three )

        next_ = response.css('a.nav:contains("Next")::attr("href")').extract_first()

        if next_:
            yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_two)


    def parse_three(self, response):
        # print(response.url)

        try:

            firm =  response.css("h1.HjBfq::text").extract_first()

            url = response.css("a.YnKZo.AYHFM").extract_first()

            print(url)

            # address = response.css(".kDZhm .YnKZo span.yEWoV::text").extract_first()

            # phone = response.css("a span span.yEWoV::text").extract_first()

            # if address:
            #     address = address.strip()            

            # details = {'Source': 'https://www.tripadvisor.com/', 'Firm': firm, 'URL': url,'Address Line 1': address, 'Phone': phone}

            # print(details)
      
            # mycol.insert_one(details)
        
        except Exception as e:
            print(e)
        
        return  
    
   



