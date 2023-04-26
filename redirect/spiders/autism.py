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


class QuotesSpider(scrapy.Spider):
    name = "autism"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/hypnotic.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 609): 
            # print(url_)
            yield scrapy.Request(url=f'https://www.autism.org.uk/directory/search-results?searchTerm=&postalcode=&radius=20&page={i}', callback=self.parse_one , dont_filter=True)
            

    def parse_one(self, response):

        company_links = response.css('div.results__content a::attr("href")').extract()

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two, dont_filter=True)       
        

    
    def parse_two(self, response):
        try:
            firm = response.css("h1.provider__title::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        try:
            name = response.css("h1.provider__title::text").extract_first()
        except Exception as e:
            print(e)
            name = None
        try:
            url = response.css("a[title='Contact website']::attr('href')").extract_first()
        except Exception as e:
            print(e)
            url  = None
        try:
            emails = response.css("p.provider__contact-description::text").extract()
            for email_ in emails:
                if "@" in email_:
                    print(email_)
                    email = email_
                    break
        except:
            email = None
        # try:
        #     phones = response.css("p.provider__contact-description::text").extract()
        #     for phone_ in phones:
        #         if phone_.isalpha() == True:
        #             phone = phone_
        #             break
        # except:
            phone = None
        # print(phone)
        # try:
        #     address =  response.xpath("/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[1]::text").extract().strip() 
        # except Exception as e:
        #     print(e)
        #     address = None
        # print(address)
        

        details = {'Source': 'https://www.autism.org.uk/', 'Firm': firm, 'Name': name, 'URL': url, 'Email Address': email, 'Country': 'United Kingdom'}


        print(details)

        company_details.append(details)

        print(len(company_details))
    
    
    

       
    
    
   



