import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["trust"]

mycol = mydb["trust"]


company_list = []

company_details = []

links = ['https://uk.trustpilot.com/review/www.thesixpackrevolution.com']

class QuotesSpider(scrapy.Spider):
    name = "trust"
 
   
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        # json_data = json.dumps(company_details, ensure_ascii=False)
        # json_data = json_data.replace('\\"', "")
        # with open(f"output/sweden.json", "w", encoding="utf-8") as out:
        #     out.write(json_data)
    
    def start_requests(self):
        yield scrapy.Request(url=links[0], callback=self.parse_one)


    def parse_one(self, response):

        links = response.css('a.styles_consumerDetails__ZFieb::attr("href")').extract()

        for link in links:      
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two)

        next = response.css('a:contains("Next page")::attr("href")').extract_first()

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_one)
    

    def parse_two(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            print(firm)

            email = response.css('a.typography_body-m__xgxZ_.typography_appearance-action__9NNRY::attr("href")').extract_first()

            print(email)

            # address = response.css('li.class="styles_contactInfoElement__SxlS3"::text').extract_first()

            # details = {'Source': 'https://www.misterwhat.co.uk/', 'Firm': firm, 'Email Address': email,
            #          'Address Line 1': address}

            # print(details)

            # mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
