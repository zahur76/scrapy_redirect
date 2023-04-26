import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["glassdoor"]

mycol = mydb["glassdoor"]



class QuotesSpider(scrapy.Spider):
    name = "glassdoor"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    
    def start_requests(self):
        # 201
        for i in range(1, 111):
            yield scrapy.Request(url=f'https://www.glassdoor.com/Explore/browse-companies.htm?overall_rating_low=3.5&page={i}&locId=567&locType=M&locName=Minneapolis-St.%20Paul,%20MN&sector=10015&filterType=RATING_OVERALL', callback=self.parse_two)

    
    def parse_two(self, response):
        links = response.css('a[data-test=cell-Reviews-url]::attr("href")').extract()


        for link in links:          
            yield scrapy.Request(url=response.urljoin(link.replace('Reviews-', 'EI_I').replace('Reviews', 'Overview')), callback=self.parse_three, meta={'page': response.url})


    def parse_three(self, response):

        print(response.url)    
        

        data = json.loads(response.xpath('//*[@id="PageBodyContents"]/div/script[1]//text()').extract_first())

        try:

            details = {'Source': 'https://www.glassdoor.co.uk/', 'Firm': data['itemReviewed']['name'], 'URL': data['itemReviewed']['sameAs']}

            print(details)
            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
