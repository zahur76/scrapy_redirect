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
    name = "choice"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/choice.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 15860+1):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.charitychoice.co.uk/charities/england?pid={i}', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('div.sp-content h2 a::attr("href")').extract()

        print(len(links))

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)

        try:
            firm = response.css('h1::text').extract_first().strip()
            # print(firm)
            url = response.css('span[itemprop=url] a::attr("href")').extract_first()
            # print(url)

            linkedin = response.css('p.url-linkedin a::attr("href")').extract_first()
            # print(url)
            address = response.css('span[itemprop=street-address]::text').extract_first().strip()

            email = response.css('span[itemprop=email]::text').extract_first()

            # print(email)
            phone = response.css('span[itemprop=tel]::text').extract_first()

            city = response.css('[itemprop=locality]::text').extract_first().strip()

            postal = response.css('[itemprop=postal-code]::text').extract_first().strip()


            details = {'Source': 'https://www.charitychoice.co.uk/', 'Firm': firm, 'URL': url, 'Linkedin URL': linkedin, 'Email Address': email,
                        'Tellephone Number': phone, 'Address Line 1': address, 'City': city, 'Postal Code': postal}

            print(details)
            company_details.append(details)           

            print(len(company_details))

            company_details.append(details)
        except Exception as e:
            print(f'{e}')
