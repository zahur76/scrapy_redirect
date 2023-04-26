import scrapy
import pymongo
from pymongo import MongoClient
from scrapy import signals
from scrapy.selector import Selector



mongo = 'mongodb://localhost:27017/'
client = MongoClient(mongo)
db = client.Scrapy_database_whole
data = db.data_pharmaceutical

class QuotesSpider(scrapy.Spider):
    name = "pharm"


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    # here is where we set pagination in initial url as well
    def start_requests(self):
        # for i in range(1, 200):
        yield scrapy.Request(url=f'https://www.pharmaceutical-technology.com/contractors/lab_equip/systag/products/az/', callback=self.parse_one)

    # here we specify css selector for links and load the page for us
    def parse_one(self, response):
        company_links = response.css("h4 a::attr('href')").extract()
        
    # we can also use extract_first() here
        for company in company_links:
            print(company)
            # Here we will use urljoin in order to build a complete url from 2 parts. To be tested with complete url in links
            # yield scrapy.Request(url=response.urljoin(company), callback=self.parse_two, dont_filter=True)
            yield scrapy.Request(url=company , callback=self.parse_two)

    def parse_two(self, response):

        print(response.url)
        # firm = response.css("h1::text").extract_first()

        # url = response.css("div.cell:contains('ebsite')a::attr('href')").extract_first()

        # email = response.css("div.cell:contains('ebsite')a::attr('href')").extract_first()

        # address = response.css("div.title:contains('dress') + div.description::text").extract()

        # details = {'Source': 'https://www.pharmaceutical-technology.com/',
        #            'Firm': firm.strip(),
        #            'URL': url,
        #            'Email Address': email,
        #            'Address Line 1': ' '.join(address).strip(),
        #            'Business Sector 1': 'pharmaceutical technology'}

        # print(details)
        # now save it the way you like it
        # data.insert_one(details)

        return