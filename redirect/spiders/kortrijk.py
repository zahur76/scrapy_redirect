import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["kortrijk"]

mycol = mydb["kortrijk"]


class QuotesSpider(scrapy.Spider):
    name = "kortrijk"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    
    def start_requests(self):
        for i in range(1, 600):          
            yield scrapy.Request(url=f'https://www.kortrijk.be/bedrijvengids?page={i}', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.company > a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):   
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('.field--field-website a::attr("href")').extract_first()

            email = response.css('.field--field-email.field--type--companyguide-field a::attr("href")').extract_first()

            address = response.css('div.address-1::text').extract_first()

            details = {'Source': 'https://www.kortrijk.be/', 'Firm': firm, 'URL': url, 'Email Address': email,
                     'Address Line 1': address.strip()}

            print(details)

            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
