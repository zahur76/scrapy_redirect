import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []


class QuotesSpider(scrapy.Spider):
    name = "chem"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/chem.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(0, 1240):          
            yield scrapy.Request(url=f'https://www.chemeurope.com/en/companies/p{i}/', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('a.search-item-box::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):   
        try:
            firm = response.css('h1::text').extract_first()

            phone = response.css('a:has(.icon-phone)::attr("href")').extract_first()

            url = response.css('[target] .mb-2 span::text').extract_first()

            # email = response.css('a#email_link::attr("href")').extract_first()

            address_ = response.css('.js-scroll-to-element span::text').extract()


            details = {'Source': 'https://www.chemeurope.com/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                        'Address Line 1': ' '.join(address_).strip()}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
