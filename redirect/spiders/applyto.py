import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["applyto"]

mycol = mydb["applyto"]



class QuotesSpider(scrapy.Spider):
    name = "applyto"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    
    def start_requests(self):
        for i in range(1,797):          
            yield scrapy.Request(url=f'https://www.applytosupply.digitalmarketplace.service.gov.uk/g-cloud/search?page={i}&lot=cloud-support', callback=self.parse_two)



    def parse_two(self, response):
        
        links = response.css('.govuk-heading-s a::attr("href")').extract()

        print(len(links))
        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'page': response.url})

       

    def parse_three(self, response):

        # print(response.url) 
        try:
            firm = response.css('p.govuk-body-s span.govuk-visually-hidden::text').extract_first()

            name = response.css('#meta p:nth-of-type(5)').extract_first()

            email = response.css('a[data-event-category="Email a supplier"]::attr("href")').extract_first()

            details = {'Source': 'https://www.hotfrog.co.uk/', 'Firm': firm, 'Email Address': email, 'Name': name}

            print(details)
    

            # mycol.insert_one(details)         

        except Exception as e:
            print(f'{e}')
