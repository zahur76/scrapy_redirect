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

mydb = myclient["evintra"]

mycol = mydb["evintra"]


class QuotesSpider(scrapy.Spider):
    name = "evintra"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        

    def start_requests(self):
        
        yield scrapy.Request(url=f'https://south-africa.searchinafrica.com/directory', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".main-categories a::attr('href')").extract()
        

        print(len(company_links))
        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)


    
    def parse_three(self, response):
        # print(response.url)
        company_links = response.css(".list-entryInfoBar a::attr('href')").extract()
        

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_four, dont_filter=True)

        next_ = response.css('a:contains(">)::attr("href")').extract_first()

        if next_:
            yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_three , dont_filter=True)

    def parse_four(self, response):
        print(response.url)

        try:

            firm =  response.css("h1::text").extract_first()

            script_ = response.css(".email script").extract_first()


            if script_:
                
                try:
                    js = script_.replace('<script type="text/javascript">', '').replace('//<![CDATA[', 'function escramble_758(){var zahur=[];').replace('//]]>', '').replace('</script>', 'return zahur } escramble_758()').replace("document.write", "zahur.push")

                    email = str(converter(js.strip()))

                    print(email)
                except:
                    email = None
            else:
                email = None

            url = response.css(".web a::attr('href')").extract_first()    

            address = response.css("div.address_1::text").extract_first()

            if address:
                address = address.strip()            

            details = {'Source': 'https://south-africa.searchinafrica.com/', 'Firm': firm, 'Email Address': email, 'URL': url,'Address Line 1': address, 'Country' : 'South Africa'}

            print(details)

      
            # mycol.insert_one(details)
        
        except Exception as e:
            print(e)
        
        return  
    
   



