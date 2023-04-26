import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv
import json
import os


links = pd.read_csv('input/redirect.csv')

redirect_dict = {}

# start_urls = ['https://www.superpages.com/las-vegas-nv/credit-debt-counseling?',
#                 'https://www.superpages.com/new-york-ny/insurance?',
#                 'https://www.superpages.com/las-vegas-nv/accountants-certified-public?',
#                 'https://www.superpages.com/las-vegas-nv/loans?',
#                 'https://www.superpages.com/las-vegas-nv/mortgages?',
#                 'https://www.superpages.com/las-vegas-nv/bookkeeping?',
#                 'https://www.superpages.com/las-vegas-nv/stock-bond-brokers?',
#                 'https://www.superpages.com/las-vegas-nv/financial-planning-consultants?']


start_urls = [
                'https://www.emdria.org/directory/?fwp_paged=1'
               ]


company_list = []

company_details = []

count = []


class QuotesSpider(scrapy.Spider):
    name = "emdria"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/emdria.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for url_ in start_urls: 
            print(url_)
            for i in range(1, 109): #109
                url_ = f'https://www.emdria.org/directory/?fwp_paged={i}' 
                yield scrapy.Request(url=url_, callback=self.parse_one , dont_filter=True)
            

    def parse_one(self, response):

        comnpany_links = response.css("div.directory-listing-name a::attr('href')").extract()

        print(len(comnpany_links))

        for link in comnpany_links:
            yield scrapy.Request(url=link, callback=self.parse_two, dont_filter=True)


    def parse_two(self, response):

        try:
            firm =  response.css("div.ycd-connected-organization::text").extract_first().strip() 
        except Exception as e:
            print(e)
            firm = None
        try:
            name=  response.css("h2.indiv-name::text").extract_first().strip() 
        except Exception as e:
            print(e)
            name = None
        # print(firm)
        try:
            url = response.css("div.fl-icon-text a::attr('href')").extract_first().strip() 
        except Exception as e:
            print(e)
            url  = None
        try:
            email = response.css("button.indiv-email-button::attr('data-ycd-individual-email')").extract_first()
        except:
            email = None
        # print(url)
        try:
            phone = response.css("div.ycd-phone-number a::text").extract_first()
        except:
            phone = None
        # print(phone)
        try:
            address = response.css("div.address a::text").extract_first().strip()
        except:
            address = None
        # print(address)
        

        details = {'Source': 'https://www.emdria.org', 'Firm': firm, 'Name': name, 'URL': url, 'Email Address': email, 'Telephone Number': phone, 'Address Line 1': address}


        print(details)

        company_details.append(details)

        print(len(company_details))

           
    #     # try:
    #     #     next = response.css('a.next.ajax-page::attr("href")').extract()
    #     # except:
    #     #     next = None
        
    #     # if next:
    #     #     print(next[0])
    #     #     yield scrapy.Request(url=response.urljoin(next[0]), callback=self.parse_one, dont_filter=True)
        
        return
        
    
    
    

       
    
    
   



