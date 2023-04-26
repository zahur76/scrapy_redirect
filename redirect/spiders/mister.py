import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mister"]

mycol = mydb["mister"]


company_list = []

company_details = []

links = ['https://www.gladiatorbusiness.co.uk/all-categories']

class QuotesSpider(scrapy.Spider):
    name = "mister"
    custom_settings = {
        'DOWNLOAD_DELAY': 25,
        'CONCURRENT_REQUESTS': 1
    }
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
  
        mainlink = f'https://www.misterwhat.co.uk/greater-london/london/876_london'
        yield scrapy.Request(url=mainlink, callback=self.parse_one)


    def parse_one(self, response):

        links = response.css('.citylist a[data-skpa]::attr("href")').extract()


        for link in links:      
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two)

    
    def parse_two(self, response):

        c_links = response.css('a[itemprop="name"]::attr("href")').extract()

        for link in c_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)

        next = response.css('a:contains("»")::attr("href")').extract_first()

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_two)
    

    def parse_three(self, response):

        try:
            firm = response.css('.h2 span::text').extract_first()

            url = response.css('.col-sm-9 a[target]::attr("href")').extract_first()

            # email = response.css('p a[href^=mail]::attr("href")').extract_first()

            phone = response.css('span[itemprop="telephone"]::text').extract_first()

            address = response.css('span[itemprop="streetAddress"]::text').extract_first()

            city = response.css('a[itemprop="addressLocality"]::text').extract_first()

            phone = response.css('[itemprop="telephone"] a::attr("href")').extract_first()

            postal = response.css('span[itemprop=""postalCode]::text').extract_first()

            details = {'Source': 'https://www.misterwhat.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Email Address': response.meta['email'],
                     'Address Line 1': address, 'City': city, 'Postal Code': postal, 'Telephone': phone}

            print(details)

            # mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
