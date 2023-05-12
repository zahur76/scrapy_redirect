import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["spoke"]

mycol = mydb["Mining"]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "spoke"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 2):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.spoke.com/search?page={i}&q=irrigation&type=company&utf8=%E2%9C%93', callback=self.parse_two)
            
    def parse_two(self, response):

        links = response.css('.sr-title a::attr("href")').extract()

        print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        try:
            firm = response.css('h1::text').extract_first().strip()
            print(firm)
            url = response.css('div.sub-profile span.web-small + a::attr("href")').extract_first()
            print(url)
            address = response.css('span[itemprop=streetAddress]::text').extract_first().strip()

            email = response.css('span[itemprop=email] a::attr("href")').extract_first()

            print(email)
            # phone = response.css('span.telephone-small +::text').extract_first()

            city = response.css('[itemprop=addressLocality] a::text').extract_first()

            state = response.css('[itemprop=addressRegion] a::text').extract_first()


            details = {'Source': 'https://www.spoke.com/', 'Firm': firm, 'URL': url, 'Email Address': email,
                        'Address Line 1': address, 'City': city, 'State Or County': state, 'Business Sector 1': 'Irrigation'}

            print(details)
            # mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')

