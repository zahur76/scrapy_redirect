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
                'https://zencare.co/locations'
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
    name = "yellowpages"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/yellowpages.json", "w", encoding="utf-8") as out:
            out.write(json_data)


    def start_requests(self):
        for i in range(1, 45):           
            yield scrapy.Request(url=f'https://www.yellowpages.com.au/search/listings?clue=counsellors&locationClue=All+States&pageNumber={i}', callback=self.parse_one)
            

    def parse_one(self, response):

        company_panel = response.css("div.MuiCard-root").extract()

        print(len(company_panel))
        
        try:
            for company in company_panel:
                url = None
                phone = None
                try:
                    firm = Selector(text=company).css("h3::text").extract_first().strip()
                except Exception as e:
                    print(e)
                    firm = None

                try:
                    url = Selector(text=company).css("a.MuiButton-textSecondary::attr('href')").extract_first()
                except Exception as e:
                    print(e)
                    url = None
                    
                try:
                    address =  Selector(text=company).css("a.MuiTypography-root p.MuiTypography-root::text").extract_first().strip() 
                except Exception as e:
                    print(e)
                    address = None

                # try:
                #     phone = response.xpath("div:nth-of-type(n+7) p.MuiTypography-colorTextSecondary::text").extract().strip() 
                # except Exception as e:
                #     print(e)
                #     phone = None
                

                details = {'Source': 'https://www.yellowpages.com.au/', 'Firm': firm, 'URL': url, 'Address Line 1': address}


                print(details)

                company_details.append(details)

                print(len(company_details))

        except Exception as e:
            print(e)


   



    
    
    
   



