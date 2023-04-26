import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["travelweekly"]

mycol = mydb["travelweekly"]


class QuotesSpider(scrapy.Spider):
    name = "travelweekly"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        # json_data = json.dumps(company_details, ensure_ascii=False)
        # json_data = json_data.replace('\\"', "")
        # with open(f"output/europages_pharmaceutical.json", "w", encoding="utf-8") as out:
        #     out.write(json_data)

    def start_requests(self):
        for i in range(1, 22892):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.travelweekly.com/Hotels/Advanced?pg={i}', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".col-sm-6 a.title::attr('href')").extract()   

        print(len(company_links))

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        # print(response.url)
        try:
            firm =  response.css("h1::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        # print(firm)
        try:
            url = response.css("a[title='Hotel Website']::attr('href')").extract_first()
        except:
            url = None

        try:
            email = response.css("a[title='Hotel E-mail']::attr('href')").extract_first()
        except:
            email = None

        try:
            address = response.css("div.address::text").extract_first()
        except:
            address = None
        
        if address:
            address.strip()

        

        details = {'Source': 'https://www.travelweekly.com/', 'Firm': firm.strip(), 'URL': url, 'Email Address': email, 'Address Line 1': address}

        print(details)

        mycol.insert_one(details)  
        
        return

   



