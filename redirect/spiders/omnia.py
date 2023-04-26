import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json


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
    name = "omnia"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/omnia.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 238):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.omnia-health.com/exhibitordirectory?page={i}', callback=self.parse_two)
            

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("a.more-link::attr('href')").extract()

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        # print(response.url)
        try:
            firm =  response.css(".section-two h1::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        # print(firm)

        url = response.css("div.field-item a::attr('href')").extract_first()
       

        address = response.css("div.thoroughfare::text").extract_first()
    

        city = response.css("div.locality::text").extract_first()

        country = response.css("span.country::text").extract_first()
      
        

        details =  {'Source': 'https://www.omnia-health.com/', 'Firm': firm.strip(), 'URL': url, 'Address Line 1': address, 'City': city,
        'Country': country, 'Business Sector 1': 'health centres'}

        print(details)

        company_details.append(details)

        print(len(company_details))
        
        return