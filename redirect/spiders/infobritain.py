import scrapy
import pymongo
from pymongo import MongoClient
from scrapy import signals
from scrapy.selector import Selector



mongo = 'mongodb://localhost:27017/'
client = MongoClient(mongo)
db = client.Scrapy_database_whole
data = db.infobritain

class QuotesSpider(scrapy.Spider):
    name = "information"


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    def start_requests(self):
        # for i in range(0, 7):
        yield scrapy.Request(url="https://www.information-britain.co.uk/attractions.cfm?county=38", callback=self.parse_one)
    # here is where we set pagination in initial url as well
    # def start_requests(self):
    #     for i in range(0, 7):
    #         yield scrapy.Request(url=f'https://www.swissbiotech.org/companies/?pg={i}&sort=a-z-featured', callback=self.parse_one)

    # here we specify css selector for links and load the page for us
    def parse_one(self, response):

        company_links = response.css("#main ul li a::attr('href')").extract()
    # we can also use extract_first() here

        for company in company_links:
            print(company)
            # Here we will use urljoin in order to build a complete url from 2 parts. To be tested with complete url in links
            # yield scrapy.Request(url=response.urljoin(company), callback=self.parse_two, dont_filter=True)
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_two, dont_filter=True)

    def parse_two(self, response):
        firm = response.css("strong::text").extract_first()

        url = response.css("a:contains('ebsite')::attr('href')").extract_first()

        email = response.css("span:contains('email') a::attr('href')").extract_first()

        address = response.css("span[itemprop='address']::text").extract()

        details = {'Source': 'information-britain.co.uk/',
                   'Firm': firm.strip(),
                   'URL': url,
                   'Email Address': email,
                   'Address Line 1': ' '.join(address).strip(),
                   'Country': 'United Kingdom',
                   'Business Sector 1': 'Attractions'}

        print(details)
        # now save it the way you like it
        # data.insert_one(details)

        return



# run with the command "scrapy crawl information (--nolog <to reduce noise in the console>) "








