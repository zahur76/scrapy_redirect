import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["deguiser"]

mycol = mydb["deguiser"]


company_list = []

company_details = []

class QuotesSpider(scrapy.Spider):
    name = "deguiser"
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
        for i in range(1, 401):
            mainlink = f'https://www.degulesider.dk/-/firmaer/{i}'
            yield scrapy.Request(url=mainlink, callback=self.parse_four)


    def parse_four(self, response):

        elements = response.css('div.MuiPaper-elevation.MuiPaper-rounded').extract()

        for element in elements:
            try:
                firm = Selector(text=element).css('.css-13kavrm a.MuiTypography-inherit::text').extract_first()
                print(firm)
                url = Selector(text=element).css('a.css-7wjnjd::attr("href")').extract_first()

                # email = response.css('p a[href^=mail]::attr("href")').extract_first()

                address = Selector(text=element).css('div.MuiBox-root.css-35dwn7::text').extract_first()


                details = {'Source': 'https://www.degulesider.dk/', 'Firm': firm, 'URL': url,
                        'Address Line 1': address}

                print(details)
                company_list.append(details)
                print(len(company_list))

                mycol.insert_one(details)

            except Exception as e:
                print(f'{e}')
    

        
