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


start_urls = [
                'https://www.bacp.co.uk/search/Therapists?UserLocation=&q=children&LocationQuery=&Location=&FoundLocation=&SortOrder=0&TherapistSortOrderSelectionMade=false&Distance=100&skip=0',
                'https://www.bacp.co.uk/search/Therapists?UserLocation=&q=children&LocationQuery=&Location=&FoundLocation=&SortOrder=0&TherapistSortOrderSelectionMade=false&Distance=100&skip=10'
                ]

count = []

company_details = []

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "bacp"

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
        page_list = list(range(0, 14080, 10))
        for page in page_list:          
            yield scrapy.Request(url=f'https://www.bacp.co.uk/search/Therapists?UserLocation=&q=children&LocationQuery=&Location=&FoundLocation=&SortOrder=0&TherapistSortOrderSelectionMade=false&Distance=100&skip={page}', callback=self.parse_one)
            

    def parse_one(self, response):

        comnpany_links = response.css("h3.search-result__title a::attr('href')").extract()

        for link in comnpany_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_two, dont_filter=True)


    def parse_two(self, response):

        try:
            firm = response.css("h1.template-directory__name::text").extract_first().strip() 
        except Exception as e:
            print(e)
            firm = None
        print(firm)
        try:
            name = response.css("h1.template-directory__name::text").extract_first().strip() 
        except Exception as e:
            print(e)
            name = None
        print(name)
        try:
            url = response.css("a[itemprop='url']::attr('href')").extract_first().strip() 
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
            phone = response.css("dd[itemprop='telephone']::text").extract_first().strip() 
        except:
            phone = None
        # print(phone)
        try:
            address =  response.css("span[itemprop='streetAddress']::text").extract_first().strip() 
        except:
            address = None

        try:
            code =  response.css("span[itemprop='postalCode']::text").extract_first().strip() 
        except:
            code = None
        # print(address)
        

        details = {'Source': 'https://www.emdria.org', 'Firm': firm, 'Name': name, 'URL': url, 'Telephone Number': phone, 'Address Line 1': address, 'Postal Code': code}


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
        
    
    
    

       
    
    
   



