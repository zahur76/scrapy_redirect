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
    name = "great"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/great.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):       
        yield scrapy.Request(url=f'https://greatnonprofits.org/nonprofits/0_9/1', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('ul > li >a::attr("href")').extract()

        for link in links:
            if '/nonprofits/' in link:
                # print(link[:-1])
                for i in range(1, 20):
                    yield scrapy.Request(response.urljoin(f'{link[:-1]}{i}'), callback=self.parse_three)
        

    def parse_three(self, response):

        print(response.url)
        company_links = response.css('ul.state-list li > a::attr("href")').extract()

        for link in company_links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_four)
    

    def parse_four(self, response):

        try:
            firm = response.css('h1[itemprop=name]::text').extract_first().strip()
            # print(firm)
            url = response.css('a.link-shortcut::attr("href")').extract_first()
            # print(url)

            # linkedin = response.css('p.url-linkedin a::attr("href")').extract_first()
            # print(url)
            address = response.css('span[itemprop=streetAddress]::text').extract_first().strip()

            email = response.css('a[itemprop=email]::attr("href")').extract_first()

            # print(email)
            # phone = response.css('span[itemprop=tel]::text').extract_first()

            city = response.css('[itemprop=addressLocality]::text').extract_first().strip()

            postal = response.css('[itemprop=postalCode]::text').extract_first().strip()

            country = response.css('[itemprop=addressCountry]::text').extract_first().strip()


            details = {'Source': 'https://greatnonprofits.org/', 'Firm': firm, 'URL': url, 'Country': country, 'Email Address': email,
                        'Address Line 1': address, 'City': city, 'Postal Code': postal}

            print(details)
            company_details.append(details)           

            print(len(company_details))

            company_details.append(details)

        except Exception as e:
            print(f'{e}')
