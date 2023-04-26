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
    name = "bridalresouces"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/bridalresources.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):        
        yield scrapy.Request(url=f'https://bridalresources.com/UK/', callback=self.parse_two)
        
    def parse_two(self, response):

        links = response.css('.clear li a::attr("href")').extract()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        # print(response.url)

        links_ = response.css('.clear li a::attr("href")').extract()

        if len(links_) == 0:
            yield scrapy.Request(url=response.url, callback=self.parse_five, dont_filter=True)
        else:
            for link in links_:
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_four, dont_filter=True)
       
    def parse_four(self, response):
        # print(response.url)
        company_links = response.css('dt > a').extract()

        for link in company_links:
            firm = Selector(text=link).css("::text").extract_first().strip()
            url = Selector(text=link).css("::attr('href')").extract_first().strip()

            details = {'Source': 'https://bridalresources.com/UK/', 'Firm': firm, 'URL': url, 'Country': 'United Kingdom'}


            # print(details)

            company_details.append(details)

        try:
            next = response.css('div.paging a::attr("href")').extract()

            max_page = []
            for next_ in next:
                max_page.append(next_.split('page-')[1].replace('.html', ''))

            for i in range(2, int(max(max_page))+1):
                # print(f'{response.url}page-{i}.html')
                yield scrapy.Request(url=f'{response.url}page-{i}.html', callback=self.parse_five, dont_filter=True)
        except:
            pass


    def parse_five(self, response):
        try:
            print(response.url)
            company_links = response.css('dt > a').extract()
            print(company_links)
            for link in company_links:
                firm = Selector(text=link).css("::text").extract_first().strip()
                url = Selector(text=link).css("::attr('href')").extract_first().strip()

                details = {'Source': 'https://bridalresources.com/UK/', 'Firm': firm, 'URL': url, 'Country': 'United Kingdom'}


                print(details)

                company_details.append(details)
        except Exception as e:
            print(e)
    
    
   



