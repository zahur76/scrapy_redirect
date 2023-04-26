import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

company_list = []

company_details = []

count = []

required_list = [
    "Aberdeen.htm",
    "Dundee.htm",
    "Edinburgh.htm",
    "Glasgow.htm",
    "Inverness.htm",
    "Perth.htm",
    "Stirling.htm",
    "Other.htm",
    "engfirms.html",
    "otherfirms.html",
    "serarbitrator.html",
    "seradebt.html",
    "serexpert.html",
    "serpatent.html",
    "shoff.htm",
    "sersurveyors.html"

]

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "scottish"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/scottish.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 2): #564
            # print(url_)
            yield scrapy.Request(url=f'https://www.scottishlaw.org.uk/lawfirms/index.html', callback=self.parse_two, dont_filter=True)
            
        
    def parse_two(self, response):

        company_links = response.css('a::attr("href")').extract()

        # print(company_links)

        for link in company_links:
            if link in required_list:
                required_list.remove(link)
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        print(response.url)

        elements = response.css('td p a').extract()

        print(len(elements))

        for element in elements:
            try:
                try:
                    firm = Selector(text=element).css("::text").extract_first().strip()
                except Exception as e:
                    print(e)
                    firm = None
                try:
                    url = Selector(text=element).css("::attr('href')").extract_first()
                except Exception as e:
                    print(e)
                    url = None
                

                details = {'Source': 'https://www.scottishlaw.org.uk/', 'Firm': firm, 'URL': url, 'Country': 'United Kingdom'}


                print(details)

                company_details.append(details)

                print(len(company_details))
        
            except Exception as e:
                print(e)
        

       
    
    
   



