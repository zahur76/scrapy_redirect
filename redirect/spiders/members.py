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

links = ['https://www.memberlinks.co.uk/locations/bedfordshire/'
]


class QuotesSpider(scrapy.Spider):
    name = "members"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/members.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:
            for i in range(1, 1913):          
                yield scrapy.Request(url=f'{link}/?page={i}', callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('div.listing_results_title a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })

        

    def parse_three(self, response): 
        
        # print(response.url)
        try:
            firm = response.css('.listing-details > strong::text').extract_first()

            phone = response.css('.listing > span::text').extract_first()
            
            url_ = response.css('a#listing_www::attr("href")').extract_first()


            # details = {'Source': 'https://www.memberlinks.co.uk/', 'Firm': firm, 'URL': url_, 'Telephone Number': phone,
            #         'State Or County': 'Bedfordshire'}

            # print(details)

            # company_details.append(details)           

            # print(len(company_details))

            # mycol.insert_one(details)

            yield scrapy.Request(url=response.urljoin(url_), callback=self.get_url, meta={'Firm': firm, 'Telephone Number': phone})

            

        except Exception as e:
            print(f'{e}')
    

    def get_url(self, response):

        details = {'Source': 'https://www.memberlinks.co.uk/', 'Firm': response.meta['Firm'], 'URL': response.url, 'Telephone Number': response.meta['Telephone Number'],
                    'State Or County': 'Bedfordshire'}

        print(details)

        company_details.append(details)           

        print(len(company_details))

        mycol.insert_one(details)