import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

company_list = []

company_details = []


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "clibrary"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/clibrary.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(0,1680,8):     
            yield scrapy.Request(url=f'https://www.charitylibrary.uk.com/all-charities/{i}', callback=self.parse_two)
        
    def parse_two(self, response):

        elements = response.css('div.nano-ui').extract()

        print(len(elements))

        for element in elements:
            # print(element)
            firm = Selector(text=element).css('div.charityTitle::text').extract_first()
            # print(firm)
            url = Selector(text=element).css('div.charityItem a::attr("href")').extract_first()
            print(url)

            name = Selector(text=element).css('div.cf:nth-of-type(3) div:nth-of-type(2)::text').extract_first()
            # print(name)
            phone = Selector(text=element).css('div:nth-of-type(n+6) div:nth-of-type(3) div:nth-of-type(4)::text').extract_first()

            # print(phone)

            address = Selector(text=element).css('div.cf:nth-of-type(5) div.grid-10::text').extract_first()


            # print(address)

            country = Selector(text=element).css('div.cf:nth-of-type(n+5) div.grid-4:nth-of-type(2)::text').extract_first()

            # print(country)

            business = Selector(text=element).css('div.cf:nth-of-type(n+5) div:nth-of-type(4)::text').extract_first()

            # print(business)


            details = {'Source': 'https://www.charitylibrary.uk.com/', 'Firm': firm, 'URL': url, 'Name': name,
                        'Telephone Number': phone, 'Address Line 1': address, 'Country': country}

            print(details)
            company_details.append(details)           

            print(len(company_details))

            company_details.append(details)
       


        
