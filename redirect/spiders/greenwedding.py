import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os

company_list = []

company_details = []


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "wedding"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/wedding.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 2): #564
            # print(url_)
            yield scrapy.Request(url=f'https://greenweddingshoes.com/wedding-artists/', callback=self.parse_two, dont_filter=True)
            
        
    def parse_two(self, response):

        company_links = response.css('.vendor-item a::attr("href")').extract()

        # print(company_links)

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):

        company_links_ = response.css('.vendor-item a::attr("href")').extract()

        # print(company_links)

        for link in company_links_:
            print(response.urljoin(link))
            # yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        print(response.body)
        try:
            try:
                firm = response.css("h2::text").extract_first().strip()
            except Exception as e:
                print(e)
                firm = None
            print(firm)
            # try:
            #     url = Selector(text=element).css("::attr('href')").extract_first()
            # except Exception as e:
            #     print(e)
            #     url = None
            

            # details = {'Source': 'https://www.scottishlaw.org.uk/', 'Firm': firm, 'URL': url, 'Country': 'United Kingdom'}


            # print(details)

            # company_details.append(details)

            # print(len(company_details))
    
        except Exception as e:
            print(e)
        

       
    
    
   



