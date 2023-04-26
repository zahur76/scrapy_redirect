import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["bunity"]

mycol = mydb["bunity"]


class QuotesSpider(scrapy.Spider):
    name = "bunity"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    def start_requests(self):
        for i in range(0, 106):            
            yield scrapy.Request(url=f'https://www.bunity.com/search?q=&category=professional-services-office-commercial-cleaning:5b4c7c149dfbc8530371d8f1&page={i}', callback=self.parse_two)


    def parse_two(self, response):
        company_links = response.css("a.businessURL::attr('href')").extract()

        for company_url in company_links:
            yield scrapy.Request(url=response.urljoin(company_url), callback=self.parse_three , dont_filter=True)

    def parse_three(self, response):
        print(response.url)

        try:
            firm =  response.css("h1.businessProfileName::text").extract_first()

            url = response.css("a.contactTarget.dont-break-out u::text").extract_first()
    
            address_1 = response.css("div.contactText::text").extract_first().strip()

            contacts = response.css('a.contactTarget::attr("href")').extract()

            phone = None


            for contact in contacts:
                if 'tel:' in contact:
                    phone = contact
            

            details = {'Source': 'https://www.bunity.com/', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Address Line 1': address_1,
            'Business Sector 1': 'Office Cleaning'}

            print(details)
      
            mycol.insert_one(details)

        except Exception as e:
            print(e)

        
        return

    
    
    

       
    
    
   



