import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["sweden"]

mycol = mydb["sweden"]


company_list = []

company_details = []

links = ['https://www.gladiatorbusiness.co.uk/all-categories']

class QuotesSpider(scrapy.Spider):
    name = "sweden"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        # json_data = json.dumps(company_details, ensure_ascii=False)
        # json_data = json_data.replace('\\"', "")
        # with open(f"output/sweden.json", "w", encoding="utf-8") as out:
        #     out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 3788):
            mainlink = f'https://www.largestcompanies.com/search?where=Sweden&page={i}'
            yield scrapy.Request(url=mainlink, callback=self.parse_four)


    def parse_four(self, response):

        elements = response.css('tbody tr').extract()

        for element in elements:
      
            link = Selector(text=element).css('span a::attr("href")').extract_first()

            email = Selector(text=element).css('a[href^="mailto"]::attr("href")').extract_first()
    
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_five, meta={'email': email})
    

    def parse_five(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('[itemprop="url"] a::attr("href")').extract_first()

            # email = response.css('p a[href^=mail]::attr("href")').extract_first()

            phone = response.css('[itemprop="telephone"] a::attr("href")').extract_first()

            address = response.css('tr:contains("Visiting address:") td[itemprop="address"]::text').extract_first().strip()

            county = response.css('tr:contains("County:") td[itemprop="location"]::text').extract_first().strip()

            phone = response.css('[itemprop="telephone"] a::attr("href")').extract_first()

            details = {'Source': 'https://www.gladiatorbusiness.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Email Address': response.meta['email'],
                     'Address Line 1': address, 'State Or County': county, 'Telephone': phone}

            print(details)
            company_list.append(details)
            print(len(company_list))

            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
