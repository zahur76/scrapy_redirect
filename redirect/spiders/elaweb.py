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
    name = "elaweb"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/elaweb.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 2): #564
            # print(url_)
            yield scrapy.Request(url=f'https://www.elaweb.org.uk/membership/directory?search=&sort_by=nameaz&page={i}', callback=self.parse_two, dont_filter=True)
            
        
    def parse_two(self, response):

        company_links = response.css('h3.person-name a::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)


    def parse_three(self, response):
        print(response.body)
        try:
            url = None
            email = None
            phone = None
            try:
                firm = response.css("h3.person-name a span::text").extract_first()
            except Exception as e:
                print(e)
                firm = None
            try:
                name = response.css("h3.person-name a span::text").extract_first()
            except Exception as e:
                print(e)
                name = None
            try:
                contacts = response.css("p.person-contact a.spamspan::attr('href')").extract()
                print(contacts)         
            except Exception as e:
                print(e)
                contacts = None
            if contacts:
                print(contacts)
                for contact in contacts:
                    if 'http' in contact:
                        url = contact.strip()

            print(response.css('a[href^="mailto"]').extract_first())
            # try:
            #     address =  response.xpath("/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[1]::text").extract().strip() 
            # except Exception as e:
            #     print(e)
            #     address = None
            # print(address)
            

            details = {'Source': 'https://www.elaweb.org.uk/', 'Firm': firm, 'Name': name,  'URL': url, 'Email Address': response.xpath('/html/body/main/div[4]/div/div[2]/div/div[1]/p[4]/a/text()').extract_first(), 'Address Line 1': response.css('p.person-contact::text').extract_first(), 'Country': 'United Kingdom'}


            print(details)

            company_details.append(details)

            print(len(company_details))
    
        except Exception as e:
            print(e)
    

       
    
    
   



