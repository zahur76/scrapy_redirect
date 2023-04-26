import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["goldenpages"]

mycol = mydb["goldenpages"]

start_urls = [
'https://www.goldenpages.be/categories/A/1/',
'https://www.goldenpages.be/categories/B/1/',	
'https://www.goldenpages.be/categories/C/1/',
'https://www.goldenpages.be/categories/D/1/',	
'https://www.goldenpages.be/categories/E/1/',
'https://www.goldenpages.be/categories/F/1/',	
'https://www.goldenpages.be/categories/G/1/',	
'https://www.goldenpages.be/categories/H/1/',	
'https://www.goldenpages.be/categories/I/1/',	
'https://www.goldenpages.be/categories/J/1/',	
'https://www.goldenpages.be/categories/K/1/',	
'https://www.goldenpages.be/categories/L/1/',	
'https://www.goldenpages.be/categories/M/1/',	
'https://www.goldenpages.be/categories/N/1/',
'https://www.goldenpages.be/categories/O/1/',	
'https://www.goldenpages.be/categories/P/1/',	
'https://www.goldenpages.be/categories/S/1/',	
'https://www.goldenpages.be/categories/T/1/',	
'https://www.goldenpages.be/categories/U/1/',	
'https://www.goldenpages.be/categories/V/1/',	
'https://www.goldenpages.be/categories/W/1/',	
'https://www.goldenpages.be/categories/Y/1/',	
'https://www.goldenpages.be/categories/Z/1/',
]


class QuotesSpider(scrapy.Spider):
    name = "goldenpages"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    
    def start_requests(self):
        for url in start_urls:        
            yield scrapy.Request(url=url, callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.gap-x-4 a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response): 
        # print(response.url)
        sector = response.url.split('/')

        print(sector)

        sector_ = sector[-1]

        if sector_ == '':
            sector_= sector[-2]
        
        print(sector_)


        links = response.css('a.right-0::attr("href")').extract()

        # for link in links:          
        #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_four)

        next_ = response.css('a.flex.cursor-pointer:has(svg)::attr("href")').extract_first()

        if next_:
            yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_three)

    
    def parse_four(self, response):
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a[title="Website"]::text').extract_first()

            address = response.css('span[itemprop="streetAddress"]::text').extract_first()

            city = response.css('span[itemprop="addressLocality"]::text').extract_first()

            details = {'Source': 'https://ingenieursbureaus.nu/', 'Firm': firm.strip(), 'URL': url.strip(),
                     'Address Line 1': address.strip(), 'City': city.strip()}

            print(details)

            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
