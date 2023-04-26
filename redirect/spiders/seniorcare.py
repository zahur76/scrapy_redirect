import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["seniorcare"]

mycol = mydb["seniorcare"]


company_list = []

company_details = []

links = ['https://seniorcarefinder.com/']


class QuotesSpider(scrapy.Spider):
    name = "seniorcare"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    
    def start_requests(self):
        for link in links:       
            yield scrapy.Request(url=link, callback=self.parse_one_half)



    def parse_one_half(self, response):
        print(response.url)
        links = response.css('a.featured-image::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two)


    def parse_two(self, response):
        print(response.url)
        links = response.css('a.seo-listing-title::attr("href")').extract()
        print(len(links))

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)

       
        next = response.css('a.page-link:contains("›")::attr("href")').extract_first()

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_two)

    def parse_three(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            phone = response.css('p#phoneNumberLink a::attr("href")').extract_first()

            url = response.css('a.provider-company-website::attr("href")').extract_first()

            address= response.css('address::text').extract_first()

            details = {'Source': 'https://seniorcarefinder.com/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                'Address Line 1': address}
            

            print(details)

            # mycol.insert_one(details)      


        except Exception as e:
            print(f'{e}')
