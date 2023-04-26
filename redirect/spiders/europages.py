import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json

# https://www.europages.co.uk/bs/transport-related-services
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["europages"]

mycol = mydb["europages_research"]


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
    name = "europages"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')


    def start_requests(self):
        for i in range(1, 11):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.europages.co.uk/companies/cat-1-testing%20of%20products%20and%20materials%20-%20institutions/pg-{i}/product%20testing.html', callback=self.parse_two)


    def parse_one(self, response):

        company_links = response.css("a.ep-ecard-serp__epage-link::attr('href')").extract()

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)

        try:
            next_page = response.css("a.ep-server-side-pagination-item::attr('href')").extract()
        except:
            next_page = None
        max_page = []
        for page in next_page:
            if 'pg' in page:
                number = find_between(page, 'pg-', '/')
                max_page.append(number)                

        print(max(max_page))
        for i in range(2,int(max(max_page))+1):
            print(next_page[1].replace('pg-2', f'pg-{str(i)}'))
            yield scrapy.Request(url=response.urljoin(next_page[1].replace('pg-2', f'pg-{str(i)}')), callback=self.parse_two, dont_filter=True)


    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("a.ep-ecard-serp__epage-link::attr('href')").extract()

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        # print(response.url)
        try:
            firm =  response.css("h1.ep-epages-header-title::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        # print(firm)
        try:
            url = response.css("a.ep-epage-sidebar__website-button::attr('href')").extract_first()
        except:
            url = None
        try:
            address = response.css("dl.ep-epages-sidebar__info p.ma-0::text").extract()
        except:
            address = None
        # print(address)
        

        details = {'Source': 'https://www.europages.co.uk', 'Firm': firm.strip(), 'URL': url, 'Address Line 1': ' '.join(address).strip(),
                   'Business Sector 1': 'Product testing'}

        print(details)

        mycol.insert_one(details)
        
        return

    
    
    

       
    
    
   



