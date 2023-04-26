import scrapy
from scrapy import signals
from scrapy.selector import Selector
from bs4 import BeautifulSoup as BS
import requests

import pandas as pd
import csv
import json , time
import cloudscraper


links = pd.read_csv('input/redirect.csv')

redirect_dict = {}

start_urls = [
                'https://www.europages.co.uk/companies/medical%20equipment.html'
               ]


# start_urls = [
           
#                 'https://www.europages.co.uk/companies/advertising%20agencies.html'
                
#                ]


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
    name = "bionity"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/bionity.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 768):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.bionity.com/en/companies/p{i}/', callback=self.parse_two)


    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("a.search-item-box::attr('href')").extract()

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):

        print(response.url)


        try:
            firm =  response.css("h1::text").extract_first()       
        
            url = response.css("i.icon-link-arrow +::text").extract_first()  

            address = response.css("i.icon-location +::text").extract_first().strip()

            phone = response.css('i.icon-phone +::text').extract_first()  

            details = {'Source': 'https://www.bionity.com/', 'Firm': firm, 'URL': url, 'Address Line 1': address,
            'Telephone Number': phone}
        except Exception as e:
            print(e)

        print(details)

        company_details.append(details)

        print(len(company_details))
        
        return

    

       
    
    
   



