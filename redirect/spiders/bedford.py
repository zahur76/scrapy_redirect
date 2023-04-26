import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://bedfordchamber.com/directory&ptgt=400&rows_per_page=400']




class QuotesSpider(scrapy.Spider):
    name = "bedford"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/bedford.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:            
            yield scrapy.Request(url=link, callback=self.parse_two)
    
    def parse_two(self, response):
        
        links = response.css('tr::attr("onclick")').extract()

        for link in links:
            print(f'https://bedfordchamber.com/directory&ID={link.split("&ID=")[1][:-2]}')
            yield scrapy.Request(url=f'https://bedfordchamber.com/directory&ID={link.split("&ID=")[1][:-2]}', callback=self.parse_three)


    def parse_three(self, response):

        print(response.url)       
        try:
            firm = response.css('.half_1_no_pad h1::text').extract_first()

            email = response.css('.link_button a[href*=mailto]::text').extract_first()


            address = response.css('.half_1_no_pad p:nth-of-type(2)::text').extract_first()

            address = " ".join(address.split())

            print(firm, email, address)


            details = {'Source': 'https://www.uksbd.co.uk/', 'Firm': firm, 'Email Addres': email,
                     'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
