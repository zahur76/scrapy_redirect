import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bedrijk"]

mycol = mydb["bedrijk"]


class QuotesSpider(scrapy.Spider):
    name = "bedrijk"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    
    def start_requests(self):
        for i in range(1, 11589):          
            yield scrapy.Request(url=f'https://www.bedrijfstelefoongids.nl/provincie/noord-brabant/page/{i}/', callback=self.parse_two)

    
    def parse_two(self, response):
        
        elements = response.css('ul#bedrijven li').extract()

        for element in elements:
            try:
                firm = Selector(text=element).css("h2.name::text").extract_first()

                url = Selector(text=element).css("span.url.rot13::text").extract_first()

                url_ = ''

                alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

                for l in url:

                    if l.isalpha():
                        new_pos = alphabet.index(l) - 13
                        url_ += alphabet[new_pos]
                    else:
                        url_ += l

                address = Selector(text=element).css("span.adres::text").extract_first()

                details = {'Source': 'https://www.bedrijfstelefoongids.nl/', 'Firm': firm, 'URL': url_,
                        'Address Line 1': address}

                print(details)

                mycol.insert_one(details)
            
            except Exception as e:
                print(e)
        