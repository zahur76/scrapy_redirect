import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["members"]

mycol = mydb["members"]

company_list = []

company_details = []

links = ['https://no.bizin.eu/'
]


class QuotesSpider(scrapy.Spider):
    name = "bizin"

    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/bizin.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:    
            yield scrapy.Request(url=link, callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('h3 a::attr("href")').extract()

        # print(len(links))
        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })


    def parse_three(self, response): 

        links = response.css('li:nth-of-type(9) a::attr("href")').extract_first()

        print(links)
        
        # print(response.url)
        # try:
        #     firm = response.css('.listing-details > strong::text').extract_first()

        #     phone = response.css('.listing > span::text').extract_first()
            
        #     url_ = response.css('a#listing_www::attr("href")').extract_first()


        #     details = {'Source': 'https://www.memberlinks.co.uk/', 'Firm': firm, 'URL': url_, 'Telephone Number': phone,
        #             'State Or County': 'Greater London'}

        #     print(details)

        #     company_details.append(details)           

        #     print(len(company_details))

        #     mycol.insert_one(details)

            # yield scrapy.Request(url=response.urljoin(url_), callback=self.get_url, meta={'Firm': firm, 'Telephone Number': phone})

            

        # except Exception as e:
        #     print(f'{e}')
    
