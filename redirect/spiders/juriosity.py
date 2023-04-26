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

tempo = []

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "jury"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/jury.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 305): 
            # print(url_)
            yield scrapy.Request(url=f'https://www.juriosity.com/directory/search?location=&page={i}&q=&specialisms=&type=barrister', callback=self.parse_two, dont_filter=True)
            
        
    def parse_two(self, response):

        company_links = response.css('div.user-summary__name a::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        
        try:
            url = None
            email = None
            phone = None
            try:
                firm = response.css("h1.user-profile-masthead__name::text").extract_first()
            except Exception as e:
                print(e)
                firm = None
            try:
                contacts = response.css("dd.text-multiline a::attr('href')").extract()            
            except Exception as e:
                print(e)
                contacts = None
            if contacts:
                for contact in contacts:
                    if 'http' in contact:
                        url = contact.strip()
                    elif 'mailto' in contact:
                        email = contact
                    elif 'tel' in contact:
                        phone = contact
            # try:
            #     address =  response.xpath("/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[1]::text").extract().strip() 
            # except Exception as e:
            #     print(e)
            #     address = None
            # print(address)
            

            details = {'Source': 'https://www.juriosity.com', 'Firm': firm, 'URL': url, 'Email Address': email, 'Phone Number': phone, 'Country': 'United Kingdom'}


            print(details)

            company_details.append(details)

            print(len(company_details))
    
        except Exception as e:
            print(e)
    

       
    
    
   



