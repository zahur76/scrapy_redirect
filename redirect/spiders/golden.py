import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["golden"]

mycol = mydb["golden"]


class QuotesSpider(scrapy.Spider):
    name = "golden"

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 10,
    #     'CONCURRENT_REQUESTS': 1
    # }


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')


    def start_requests(self):
        yield scrapy.Request(url=f'https://www.goldenpages.be/companies/abattoirs/', callback=self.parse_two)
        

    def parse_two(self, response):
        company_links = response.css("a.right-0::attr('href')").extract()

        print(len(company_links))

        # for company in company_links:
        #     yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three)

        next = response.css('a:has(svg)::attr("href")').extract_first()

        print(next)

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_two)
    

    def parse_three(self, response):
        print(response.url)
        # try:
        #     firm =  response.css("h1.ep-epages-header-title::text").extract_first()
        # except Exception as e:
        #     print(e)
        #     firm = None
        # # print(firm)
        # try:
        #     url = response.css("a.ep-epage-sidebar__website-button::attr('href')").extract_first()
        # except:
        #     url = None
        # try:
        #     address = response.css("dl.ep-epages-sidebar__info p.ma-0::text").extract()
        # except:
        #     address = None
        # # print(address)
        

        # details = {'Source': 'https://www.infobel.com/', 'Firm': firm.strip(), 'URL': url, 'Address Line 1': ' '.join(address).strip(),
        #     'Business Sector 1': 'Hardware Maintenance'}

        # print(details)

        # mycol.insert_one(details)  
        
        return

   



