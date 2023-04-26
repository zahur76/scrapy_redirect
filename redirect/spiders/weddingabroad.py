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
    name = "weddingabroad"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/weddingabroad.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 17): #564
            # print(url_)
            yield scrapy.Request(url=f'https://weddingsabroad.com/searches?sf_data=all&_sft_content_type=provider&sf_paged={i}', callback=self.parse_two)
        
    def parse_two(self, response):

        company_links = response.css('h3.elementor-post__title a::attr("href")').extract()

        print(len(company_links))

        for link in company_links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        try:
            try:
                firm = response.css("h1.elementor-heading-title::text").extract_first().strip()
            except Exception as e:
                print(e)
                firm = None
            try:
                url = response.css("a span.elementor-icon-list-text::attr('href')").extract_first()
            except Exception as e:
                print(e)
                url = None
            print(url)


            try:
                email = response.css("li:nth-of-type(2) span.elementor-icon-list-text::text").extract_first().strip()
            except Exception as e:
                print(e)
                email = None

            try:
                phone= response.css("li:nth-of-type(2) span.elementor-icon-list-text::text").extract_first().strip()
            except Exception as e:
                print(e)
                phone = None
            

            details = {'Source': 'https://www.ukbride.co.uk', 'Firm': firm, 'URL': url, 'Email Address': email, 'Telephone Number': phone}


            print(details)

            company_details.append(details)

            print(len(company_details))
    
        except Exception as e:
            print(e)
        

       
    
    
   



