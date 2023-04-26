import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bizify"]

mycol = mydb["bizify"]


class QuotesSpider(scrapy.Spider):
    name = "bizify"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        # json_data = json.dumps(company_details, ensure_ascii=False)
        # json_data = json_data.replace('\\"', "")
        # with open(f"output/bizify_A.json", "w", encoding="utf-8") as out:
        #     out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 3):          
            yield scrapy.Request(url=f'https://www.bizify.co.uk/search/financial-advisor-in-london/{i}', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('a[title*="View Business"]::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):        
        try:
            firm = response.css('h2[itemprop="name"]::text').extract_first()

            phone = response.css('[itemprop="telephone"] a::attr("href")').extract_first()

            url = response.css('a[itemprop="url"]::attr("href")').extract_first()

            address_ = response.css('span[itemprop="streetAddress"]::text').extract_first()

            county = response.css('span[itemprop="addressRegion"]::text').extract_first()

            postal = response.css('span[itemprop="postalCode"]::text').extract_first()

            details = {'Source': 'https://www.bizify.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                     'Address Line 1': address_, 'State Or County': county, 'Postal Code': postal}

            print(details)
      
            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
