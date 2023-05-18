import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["builtin"]

mycol = mydb["builtin"]


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "builtin"

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 1
    }

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        for i in range(1, 1442):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://builtin.com/companies/type/adtech-companies/app-development-companies/artificial-intelligence-companies/blockchain-companies/ecommerce-companies/edtech-companies/fintech-companies/gaming-companies/generative-ai-companies/greentech-companies/healthtech-companies/hr-tech-companies/infrastructure-as-a-service-iaas-companies/iot-companies/legal-tech-companies/machine-learning-industry-companies/marketing-tech-companies/metaverse-companies/mobile-companies/nanotechnology-companies/productivity-companies/proptech-companies/quantum-computing-companies/real-estate-companies/robotics-companies/software-companies/virtual-reality-companies/web3-companies?page={i}', callback=self.parse_two)
            
    def parse_two(self, response):

        links = response.css('.align-center a::attr("href")').extract()

        print(len(links))

        # for link in links:
        #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
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
                        'Address Line 1': address, 'City': city, 'State Or County': state, 'Business Sector 1': 'Equine'}

            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')

