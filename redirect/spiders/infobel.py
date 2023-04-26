import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["infobel"]

mycol = mydb["infobel"]


class QuotesSpider(scrapy.Spider):
    name = "infobel"

    custom_settings = {
        'DOWNLOAD_DELAY': 10,
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
        # for i in range(1, 3):
        #     print(f'page: {i}')
        yield scrapy.Request(url=f'https://www.infobel.com/en/italy/Search/BusinessResults?token=eyJDdXJyZW50UGFnZSI6MSwiUmVjb3Jkc1BlclBhZ2UiOjIwLCJDb3VudHJ5Q29kZSI6IklUIiwiQnVzaW5lc3NUeXBlIjoxLCJTb3J0QnkiOlsxXSwiU2VhcmNoVGVybSI6IkhvdGVscyIsIlNlYXJjaExvY2F0aW9uIjoidmVyb25hIiwiUmVzaWRlbnRpYWxTZWFyY2hUZXJtIjpudWxsLCJTZWFyY2hDYXRlZ29yaWVzIjp7IjAxNzEwOCI6M30sIkNhdGVnb3J5Q29kZSI6IjAxNzEwOCIsIkNhdGVnb3J5TGV2ZWwiOjMsIklzTWV0YSI6ZmFsc2UsIkxhdGl0dWRlIjpudWxsLCJMb25naXR1ZGUiOm51bGwsIk9yZGVyMDgiOm51bGwsIk9yZGVyMDkiOm51bGwsIk5lYXJCeSI6bnVsbCwiU3RyaWN0TG9jYXRpb24iOmZhbHNlLCJDYXRlZ29yeVNlYXJjaCI6ZmFsc2UsIlRvcENpdGllc051bWJlciI6MjEsIlRvcENpdGllc0FyZWEiOjMwLCJUb3BDYXRlZ29yaWVzTnVtYmVyIjoxMCwiVG9wQ29tcGV0aXRvcnNOdW1iZXIiOjAsIlRvcENvbXBldGl0b3JzQXJlYSI6MCwiVmFsaWRGb3JFbmNyeXB0aW9uIjp0cnVlLCJMb2NhdGlvbldpdGhQcm92aW5jZSI6ZmFsc2V9', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".customer-item-name a::attr('href')").extract()

        print(len(company_links))

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three)

        next = response.css('a:contains("Next")::attr("href")').extract_first()

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

   



