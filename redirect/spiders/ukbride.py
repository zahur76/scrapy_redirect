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
    name = "ukbride"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/ukbride.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 151): #564
            # print(url_)
            yield scrapy.Request(url=f'https://www.ukbride.co.uk/wedding-venues/united-kingdom?page={i}', callback=self.parse_two)
        
    def parse_two(self, response):

        company_links = response.css('.supplier-name a::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        company_links_ = response.css('.vendor-item a::attr("href")').extract()

        # print(company_links)

        for link in company_links_:
            print(response.urljoin(link))
            # yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        try:
            try:
                firm = response.css(".main-info-block_desktop h1::text").extract_first().strip()
            except Exception as e:
                print(e)
                firm = None
            try:
                url = response.css(".initial-info-block-links a::attr('href')").extract_first()
            except Exception as e:
                print(e)
                url = None
            print(url)
            try:
                county = response.css(".main-info-block_desktop h3::text").extract_first().strip()
            except Exception as e:
                print(e)
                county = None

            try:
                postal_code = response.css(".address-block li:nth-of-type(5)::text").extract_first().strip()
            except Exception as e:
                print(e)
                postal_code = None
            

            details = {'Source': 'https://www.ukbride.co.uk', 'Firm': firm, 'URL': url, 'State Or County': county, 'Postal Code': postal_code, 'Country': 'United Kingdom'}


            print(details)

            company_details.append(details)

            print(len(company_details))
    
        except Exception as e:
            print(e)
        

       
    
    
   



