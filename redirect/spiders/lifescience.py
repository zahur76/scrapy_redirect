import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []


class QuotesSpider(scrapy.Spider):
    name = "lifescience"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/lifescience.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(0, 203):          
            yield scrapy.Request(url=f'https://www.life-sciences-europe.com/organisation/Life-Sciences-Europe-EU-Germany-Organisations-Companies-List-Table-Addresses-Contacts-Austria-Switzerland-1001-95-1-{i}-1-asc.html', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('td a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):   
        try:
            firm = response.css('h1::text').extract_first()

            phone = response.css('td:contains(Tel) +::text').extract_first()

            url = response.css('div.weblink a::attr("href")').extract_first()

            # email = response.css('a#email_link::attr("href")').extract_first()

            address_ = response.css('td:contains(Street) +::text').extract_first()

            city = response.css('td:contains(City) +::text').extract_first()

            details = {'Source': 'https://www.life-sciences-europe.com/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                     'City': city, 'Address Line 1': address_,}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
