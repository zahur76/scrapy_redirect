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
                'https://www.hypnoticworld.com/hypnotherapists/'
               ]


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
    name = "hypnotic"

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
        for url_ in start_urls: 
            # print(url_)
            yield scrapy.Request(url=url_, callback=self.parse_one , dont_filter=True)
            

    def parse_one(self, response):

        country_links = response.css('div.col-6:nth-of-type(n+4) a.align-items-center::attr("href")').extract()

        for link in country_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two, dont_filter=True)


    def parse_two(self, response):

        # print(response.url)
        
        company_links = response.css('div[data-fah-results-additional-location="0"]:nth-of-type(n+2) a.btn-primary::attr("href")').extract()

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
        try:
            next = response.css('a.page-link').extract()
        except:
            next = None
        
        for nxt in next:
            if 'Next' in nxt:
                url_ = find_between(nxt, 'href="', '">').replace('amp;', '')
                # print(response.urljoin(url_))
                yield scrapy.Request(url=response.urljoin(url_), callback=self.parse_two, dont_filter=True)
    
    def parse_three(self, response):
        # print(response.url)
        try:
            firm = response.css("h1 span[itemprop=name]::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        print(firm)
        try:
            name = response.css("h1 span[itemprop=name]::text").extract_first()
        except Exception as e:
            print(e)
            name = None
        try:
            url = response.css("div.col-md-9:nth-of-type(2) a::attr('href')").extract_first().strip() 
        except Exception as e:
            print(e)
            url  = None
        print(url)
        # try:
        #     email = response.css("button.indiv-email-button::attr('data-ycd-individual-email')").extract_first()
        # except:
        #     email = None
        # print(url)
        try:
            phone = response.css("span[itemprop='telephone']::text").extract_first().strip() 
        except:
            phone = None
        # print(phone)
        # try:
        #     address =  response.xpath("/html/body/div[3]/div[1]/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[1]::text").extract().strip() 
        # except Exception as e:
        #     print(e)
        #     address = None
        # print(address)
        

        details = {'Source': 'https://www.hypnoticworld.com/', 'Firm': firm, 'Name': name, 'URL': url, 'Telephone Number': phone, 'Country': 'United States'}


        print(details)

        company_details.append(details)

        print(len(company_details))
    
    
    

       
    
    
   



