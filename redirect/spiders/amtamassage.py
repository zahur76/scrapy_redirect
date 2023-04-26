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
    name = "health"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/health.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 1911):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.amtamassage.org/find-massage-therapist/?page={i}', callback=self.parse_two)
        
    def parse_two(self, response):
        print(response.url)
        links = response.css('.find-a-mr-results-list-item-title').extract()

        print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        try:
            firm = response.css('h1.adage-heading-title::text').extract_first()
            print(firm)
            name = response.css('h1.adage-heading-title::text').extract_first()

            url = response.css('span:contains(Website) + a::attr("href")').extract_first()
            print(url)
            # address = response.css('span[itemprop=streetAddress]::text').extract_first().strip()

            # email = response.css('span[itemprop=email] a::attr("href")').extract_first()

            phone = response.css('span:contains(Phone) + a::attr("href")').extract_first()
            print(phone)
            # city = response.css('[itemprop=addressLocality] a::text').extract_first()

            # state = response.css('[itemprop=addressRegion] a::text').extract_first()


            # details = {'Source': 'https://www.amtamassage.org/', 'Firm': firm, 'Name': name, 'URL': url, 'Email Address': email,
            #             'Address Line 1': address, 'City': city, 'State Or County': state, 'Business Sector 1': 'Cosmetics'}

            # print(details)
            # company_details.append(details)           

            # print(len(company_details))

            company_details.append(details)
        except Exception as e:
            print(f'{e}')
