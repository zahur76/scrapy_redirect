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
    name = "osteopathy"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/osteopathy.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(0, 486):    
            yield scrapy.Request(url=f'https://members.iosteopathy.org/find-an-osteopath?display_name=&display_name_1=&country=All&city=&postcode_from=&from_miles=&private_health_insurers_129=&areas_of_specialism_134=&home_visits_130=All&parking_availability_125=All&page={i}', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('a.btn::attr("href")').extract()

        print(len(links))

        for link in links:
            print(link)
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.url)


        try:
            firm = response.css('h2::text').extract_first()

            name = response.css('h1::text').extract_first()
            print(firm)
            url = response.css('.views-field-url-157 a::attr("href")').extract_first()

            email = response.css('.views-field-email-156 a::attr("href")').extract_first()

            address = response.css('div.views-field-supplemental-address-1 span.field-content::text').extract_first()

            city = response.css('.views-field-city span::text').extract_first()

            postal_code = response.css('.views-field-postal-code span::text').extract_first()

            phone = response.css('.views-field-telephone-155 span.field-content::text').extract_first()

            details = {'Source': 'https://mywed.com/en/photographers/', 'Firm': firm, 'URL': url, 'Email Address': email,
                        'City': city, 'Postal Code': postal_code, 'Telephone Number': phone, 'Name': name,
                            'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

            # company_details.append(details)
        except Exception as e:
            print(f'{e}')
