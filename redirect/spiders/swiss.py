import scrapy
import pymongo
from pymongo import MongoClient
from scrapy import signals
from scrapy.selector import Selector



mongo = 'mongodb://localhost:27017/'
client = MongoClient(mongo)
db = client.Scrapy_database_whole
data = db.swissbiotech

class QuotesSpider(scrapy.Spider):
    name = "swiss"


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
    # here is where we set pagination in initial url as well
    def start_requests(self):
        for i in range(0, 7):
            yield scrapy.Request(url=f'https://www.swissbiotech.org/companies/?pg={i}&sort=a-z-featured', callback=self.parse_one)

    # here we specify css selector for links and load the page for us
    def parse_one(self, response):
        company_links = response.css("div.lf-item a::attr('href')").extract()
    # we can also use extract_first() here

        print(len(company_links))
        # for company in company_links:
        #     # Here we will use urljoin in order to build a complete url from 2 parts. To be tested with complete url in links
        #     # yield scrapy.Request(url=response.urljoin(company), callback=self.parse_two, dont_filter=True)
        #     yield scrapy.Request(url=company, callback=self.parse_two, dont_filter=True)

    def parse_two(self, response):
        firm = response.css("h1::text").extract_first()

        url = response.css("li:contains('ebsite') a::attr('href')").extract_first()

        email = response.css("li:contains('email') a::attr('href')").extract_first()

        address = response.css("div.map-block-address p::text").extract()

        details = {'Source': 'https://www.pharmaceutical-technology.com/',
                   'Firm': firm.strip(),
                   'URL': url,
                   'Email Address': email,
                   'Address Line 1': ' '.join(address).strip(),
                   'Country': 'Switzerland',
                   'Business Sector 1': 'biotech'}

        print(details)
        # now save it the way you like it
        data.insert_one(details)

        return



# run with the command "scrapy crawl europages (--nolog <to reduce noise in the console>) "