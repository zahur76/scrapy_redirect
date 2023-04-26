import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


class QuotesSpider(scrapy.Spider):
    name = "cylex"

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

    def start_requests(self):
          
        yield scrapy.Request(url=f'https://www.cylex-belgie.be/luik/', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.mb-3 a::attr("href")').extract()

        print(len(links))

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):

        links = response.css('.h4 a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_four)
    
    def parse_four(self, response):

        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a.font-base::text').extract_first()

            address  = response.css('div#cp-street span::text').extract_first()

            phone = response.css('a[aria-label="Telefoon"]::attr("href")').extract_first()

            details = {'Source': 'https://www.cylex-belgie.be/', 'Firm': firm, 'URL': url,
                     'Address Line 1': address, 'Telephone Number': phone}

            print(details)
        except Exception as e:
            print(e)
            
        
