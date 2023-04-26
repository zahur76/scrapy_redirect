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
    name = "photo"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/photo.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(0, 3540, 30):   
            yield scrapy.Request(url=f'https://www.photographerlistings.org/England/Berkshire/C1-3-1-0.htm', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('td td td td td a::attr("href")').extract()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        print(response.url)
        element = response.xpath('/html/body/table/tbody/tr[2]/td/table[2]/tbody/tr/td').extract()

        print(len(element))

    def parse_four(self, response):
        try:
            firm = response.css('div.padding h1::text').extract_first().strip()

            url = response.css('h3.light a::attr("href")').extract_first()

            address = response.css('div.padding h3.light::text').extract_first().strip()

            # country = response.css('.profile-new-head-site::attr("href")').extract_first()

            details = {'Source': 'https://www.jewelers.org/', 'Firm': firm, 'URL': url, 'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

            # company_details.append(details)
        except Exception as e:
            print(f'{e}')
