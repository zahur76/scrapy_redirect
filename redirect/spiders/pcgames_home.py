import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["pcgames"]

mycol = mydb["pcgames"]


class QuotesSpider(scrapy.Spider):
    name = "pcgames"


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
       
    def start_requests(self):
        for i in range(1, 743):
            # print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.pcgamesinsider.biz/directory/page/{i}/', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".companies h2 a::attr('href')").extract()

        # print(len(company_links))

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three)
    

    def parse_three(self, response):
        print(response.url)
        try:
            firm =  response.css("div.details h1::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        # print(firm)
        try:
            url = response.css("div.label:contains('Website') + div a::attr('href')").extract_first()
        except:
            url = None
    
        sector = response.css('div.qualifier::text').extract_first()

        details = {'Source': 'https://www.pcgamesinsider.biz/', 'Firm': firm.strip(), 'URL': url, 'Business Sector 1': sector}

        print(details)

        mycol.insert_one(details)
        
        return

   



