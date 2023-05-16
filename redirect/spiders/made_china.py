import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["china"]

mycol = mydb["china"]


class QuotesSpider(scrapy.Spider):
    name = "china"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    
    def start_requests(self):
     
        yield scrapy.Request(url='https://www.made-in-china.com/Auto-Parts-Accessories-manufacturers.html', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('li li a::attr("href")').extract()


        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)

    
    def parse_three(self, response):

        links = response.css('.company-name a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_four)
        
        next = response.css('a.next:contains("Next")::attr("href")').extract_first()

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_three)

    
    def parse_four(self, response):

        contact = response.css('a.sr-nav-title::attr("href")').extract_first()

        next_ = contact + '/contact-info.html'


        yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_five)


    def parse_five(self, response):   
        try:
            firm = response.css('h1::text').extract_first().strip()

            url = response.css('a.link-web::attr("href")').extract_first()

            address = response.css('span.contact-address::text').extract_first().strip()

            details = {'Source': 'https://www.made-in-china.com/', 'Firm': firm, 'URL': url, 'Address Line 1': address}

            print(details)

            mycol.insert_one(details)

        except Exception as e:
            print(f'{e}')
