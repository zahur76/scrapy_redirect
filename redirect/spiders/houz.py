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
    name = "houzz"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/houzz.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(0,5000,15):     
            yield scrapy.Request(url=f'https://www.houzz.com/professionals/home-builders/project-type-sustainable-design-probr1-bo~t_11823~sv_29500?fi={i}', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('div.hz-pro-search-result > a::attr("href")').extract()

        # print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        # print(response.url)

        

        # print(firm)
        # print(url)
        # print(phone)
        # print(address)

        

        try:
            firm = response.css('h1.sc-mwxddt-0::text').extract_first()

            url = response.css('span.Website__EllipsisText-sc-19fzbgj-0::text').extract_first()

            phone = response.xpath('//*[@id="business"]/div/div[2]/p/text()').extract_first()

            address = response.css('.kuSRBP p::text').extract_first()


            details = {'Source': 'https://www.houzz.com/', 'Firm': firm, 'URL': url,
                        'Telephone Number': phone, 'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
