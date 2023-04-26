import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []



class QuotesSpider(scrapy.Spider):
    name = "pets"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/pets.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):     
        yield scrapy.Request(url=f'https://www.bringfido.com/resource/?page=817', callback=self.parse_two)

    
    def parse_two(self, response):
        print(response.url)



    def parse_three(self, response):        

        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a.profile-website::attr("href")').extract_first()

            email = response.css('div.meta-card a[href^=mailto]::attr("href")').extract_first()

            address = response.css('span.js-rendered-content::text').extract_first()

            details = {'Source': 'https://architizer.com/', 'Firm': firm, 'URL': url,
                        'Email Address': email, 'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
