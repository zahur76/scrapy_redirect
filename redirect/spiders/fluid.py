import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json


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
    name = "fluid"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/fluid.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 28):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://fluidhandlingpro.com/fluid-handling-equipment-manufacturers/page/{i}/', callback=self.parse_two)
            

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css("div.top-supplier-part a.thumb::attr('href')").extract()


        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        # print(response.url)

        firm =  response.css("div.item:nth-of-type(1) span.company-entry-value::text").extract_first()
    
        # print(firm)

        url = response.css(".item a::attr('href')").extract_first()
       

        address = response.css("div:nth-of-type(3) span.company-entry-value::text").extract_first()
        
        city = response.css('div:nth-of-type(5) span.company-entry-value::text').extract_first()
        # print(address)
        
        country = response.css('div:nth-of-type(6) span.company-entry-value::text').extract_first()

        phone = response.css('div:nth-of-type(7) span.company-entry-value::text').extract_first()

        details = {'Source': 'https://fluidhandlingpro.com/', 'Firm': firm, 'URL': url, 'Address Line 1': address, 'City': city,
            'Telephone Number': phone, 'County': country, 'Business Sector 1': 'Medical Equipment'}

        print(details)

        company_details.append(details)

        print(len(company_details))
        
        return


    
    

       
    
    
   



