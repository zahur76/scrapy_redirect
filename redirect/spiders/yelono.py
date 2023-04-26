import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.yelono.com/location/%C3%85krehamn']




class QuotesSpider(scrapy.Spider):
    name = "yelono"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/yelono.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:            
            yield scrapy.Request(url=link, callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('h4 a::attr("href")').extract()

        print(len(links))
        # for link in links:          
        #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })


    def parse_three(self, response):        
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('.tjtwo a::attr("href")').extract_first()


            address_ = response.css('div.tjtwo::text').extract()


            address = ','.join(address_).strip().replace(',','').replace("\n", "")

            details = {'Source': 'https://www.uksbd.co.uk/', 'Firm': firm, 'URL': url,
                     'Address Line 1': address[:-13], 'City': response.meta['response'].replace('https://www.uksbd.co.uk/townall/', '').replace('/', '')}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
