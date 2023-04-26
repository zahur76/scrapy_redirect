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
    name = "aihitdata"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/aihitdata.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 101):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.aihitdata.com/search/companies?c=&i=life+sciences&k=&v=3&l=&p={i}&r=&t=&w=1&rc=', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('div.panel-body > div > a::attr("href")').extract()

        print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        try:
            firm = response.css('h1.text-info::text').extract_first().strip()
            print(firm)
            url = response.css('ul.list-inline > li a.::attr("href")').extract_first()
            print(url)

            # linkedin = response.css('p.url-linkedin a::attr("href")').extract_first()
            # print(url)
        #     address = response.css('span[itemprop=streetAddress]::text').extract_first().strip()

        #     email = response.css('a[itemprop=email]::attr("href")').extract_first()

        #     # print(email)
        #     # phone = response.css('span[itemprop=tel]::text').extract_first()

        #     city = response.css('[itemprop=addressLocality]::text').extract_first().strip()

        #     postal = response.css('[itemprop=postalCode]::text').extract_first().strip()

        #     country = response.css('[itemprop=addressCountry]::text').extract_first().strip()


        #     details = {'Source': 'https://greatnonprofits.org/', 'Firm': firm, 'URL': url, 'Country': country, 'Email Address': email,
        #                 'Address Line 1': address, 'City': city, 'Postal Code': postal}

        #     print(details)
        #     company_details.append(details)           

        #     print(len(company_details))

        #     company_details.append(details)

        except Exception as e:
            print(f'{e}')
