import scrapy
from scrapy import signals
from scrapy.selector import Selector


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["sourceforge"]

mycol = mydb["sourceforge"]



class QuotesSpider(scrapy.Spider):
    name = "source"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
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
        for i in range(1, 1000):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://sourceforge.net/software/usa/?page={i}', callback=self.parse_two)
            

    def parse_two(self, response):

        elements = response.css('li.project-bsl').extract()

        for element in elements:
            try:
               
                firm = Selector(text=element).css("a h3::text").extract_first().strip()
                
              
                url = Selector(text=element).css("a:contains('Visit Website')::attr('href')").extract_first()
                

                details = {'Source': 'https://sourceforge.net/', 'Firm': firm, 'URL': url, 'Country': 'USA'}


                print(details)
                mycol.insert_one(details)

        
            except Exception as e:
                print(e)
        

       
    
    
   



