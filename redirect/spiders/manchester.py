import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.yelono.com/browse-business-cities']




class QuotesSpider(scrapy.Spider):
    name = "manchester"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/manchester.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1,38+1):          
            yield scrapy.Request(url=f'https://www.visitmanchester.com/food-and-drink/searchresults?sr=1&p={i}', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.ProductName a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):   

        print(response.url)     
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a.WebsiteLink::attr("href")').extract_first()


            email = response.css('div.email::attr("href")').extract_first()

            city= response.css('.address span:nth-of-type(2)::text').extract_first()

            address  = response.css('address::text').extract_first()

            address = " ".join(address.split())


            details = {'Source': 'https://www.visitmanchester.com/', 'Firm': firm, 'URL': url,
                     'Address Line 1': address, 'City': city, 'Email Address': email}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
