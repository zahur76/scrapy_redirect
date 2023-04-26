import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os


# start_urls = ['https://www.superpages.com/las-vegas-nv/credit-debt-counseling?',
#                 'https://www.superpages.com/new-york-ny/insurance?',
#                 'https://www.superpages.com/las-vegas-nv/accountants-certified-public?',
#                 'https://www.superpages.com/las-vegas-nv/loans?',
#                 'https://www.superpages.com/las-vegas-nv/mortgages?',
#                 'https://www.superpages.com/las-vegas-nv/bookkeeping?',
#                 'https://www.superpages.com/las-vegas-nv/stock-bond-brokers?',
#                 'https://www.superpages.com/las-vegas-nv/financial-planning-consultants?']



company_list = []

company_details = []

count = []

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


black_list = ["Education & Training",
                "Expat Community Life",
                "Family Life & Living",
                "Health, Beauty & Fitness",
                "Sport & Leisure"
                ]

class QuotesSpider(scrapy.Spider):
    name = "dubai"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/anglo.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):        
        yield scrapy.Request(url=f'https://www.angloinfo.com/dubai/directory', callback=self.parse_one , dont_filter=True)
            

    def parse_one(self, response):

        company_links = response.css("ul.link-blocks li a::attr('href')").extract()

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two, dont_filter=True)
    
    
    def parse_two(self, response):

        link = response.css('li.active a::text').extract_first()

        print(link)
        if link not in black_list:
            elements = response.css('div.listing').extract()

            for element in elements:
                try:
                    firm = Selector(text=element).css('span.item-name::text').extract_first()
                except:
                    firm = None
                
                try:
                    url = Selector(text=element).css('li a[target]::attr("href")').extract_first()
                except:
                    url = None

                print(url)

        

                details = {'Source': 'https://www.angloinfo.com/', 'Firm': firm, 'URL': url, 'Country': 'UAE'}


                print(details)

                company_details.append(details)

                print(len(company_details))
    
    
    

       
    
    
   



