import scrapy
from scrapy import signals
from scrapy.selector import Selector
from redirect.spiders.test import converter

import pandas as pd
import csv
import json



start_urls = [
                'https://www.construction.co.uk/d_c/1088,-1/asbestos-removal',
                'https://www.construction.co.uk/d_c/346,-1/cleaning-services',
                'https://www.construction.co.uk/d_c/493,-1/driveway-cleaning-specialists',
                'https://www.construction.co.uk/d_c/58,-1/stone-cleaning',
                'https://www.construction.co.uk/d_c/286,-1/drain-pipe-cleaning',
                'https://www.construction.co.uk/d_c/447,-1/boiler-maintenance',
                'https://www.construction.co.uk/d_c/13,-1/property-maintenance-and-repairs',
                'https://www.construction.co.uk/d_c/697,-1/air-conditioning-service-maintenance',
                'https://www.construction.co.uk/d_c/423,-1/building-maintenance',
                'https://www.construction.co.uk/d_c/547,-1/emergency-lighting',
                'https://www.construction.co.uk/d_c/37,-1/lifts-servicing-and-repairs',
                'https://www.construction.co.uk/d_c/163,-1/lift-manufacturers',
                'https://www.construction.co.uk/d_c/524,-1/lift-and-escalator-consultants',
                'https://www.construction.co.uk/d_c/715,-1/energy-management-control-systems',
                'https://www.construction.co.uk/d_c/1039,-1/energy-management',
                'https://www.construction.co.uk/d_c/856,-1/security-doors',
                'https://www.construction.co.uk/d_c/352,-1/security-services',
                'https://www.construction.co.uk/d_c/306,-1/site-security',
                'https://www.construction.co.uk/d_c/512,-1/fire-protection-services',
                'https://www.construction.co.uk/d_c/252,-1/fire-protection-consultants-and-engineers',
                'https://www.construction.co.uk/d_c/1453,-1/waste-management',
                'https://www.construction.co.uk/d_c/302,-1/waste-disposal',
                'https://www.construction.co.uk/d_c/22,-1/heating-contractors-and-consultants',
                'https://www.construction.co.uk/d_c/32,-1/heating-equipment-sales-and-service',
                'https://www.construction.co.uk/d_c/6,-1/central-heating-installation-and-servicing',
                'https://www.construction.co.uk/d_c/69,-1/ventilation-contractors',
                'https://www.construction.co.uk/d_c/16,-1/air-conditioning-contractors',
                'https://www.construction.co.uk/d_c/697,-1/air-conditioning-service-maintenance',
                'https://www.construction.co.uk/d_c/632,-1/landscape-gardeners',
                'https://www.construction.co.uk/d_c/510,-1/lawn-turf-suppliers',
                'https://www.construction.co.uk/d_c/298,-1/project-management',
                'https://www.construction.co.uk/d_c/945,-1/tree-surgeon-and-tree-removal',
                'https://www.construction.co.uk/d_c/4,-1/plumbers']


import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["constructionuk"]

mycol = mydb["constructionquk"]


class QuotesSpider(scrapy.Spider):
    name = "construction"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')

    def start_requests(self):
        for url_ in start_urls:            
            yield scrapy.Request(url=url_, callback=self.parse_two)


    def parse_two(self, response):
        company_links = response.css("div.defaultListInfo a::attr('href')").extract()

        for company_url in company_links:
            yield scrapy.Request(url=response.urljoin(company_url), callback=self.parse_three , dont_filter=True)

        next_ = response.css('div.nextLink a::attr("href")').extract_first()

        if next_:
            yield scrapy.Request(url=response.urljoin(next_), callback=self.parse_two , dont_filter=True)

    def parse_three(self, response):
        print(response.url)
        try:
            firm =  response.css("h1::text").extract_first()

            url = response.css("div[itemprop=url] a::attr('href')").extract_first()

            script_ = response.css("div.compInfoDetail script").extract_first()

            email_ = None
            
            if script_:

                script_ = script_.replace('<script>', '').replace('document.write(emrp(', '').replace(",'construction.co.uk'));</script>", '').replace("'",'')

                email_ = ''

                for letter in script_:
                    if letter == 'A':
                        email_ += '@'
                    else:
                        email_ += chr(ord(letter) - 1)
                print(email_)
    
            address_1 = response.css("div[itemprop=streetAddress]::text").extract_first()

            address_2 = response.css("div[itemprop=addressLocality]::text").extract_first()

            address_3 = response.css("div[itemprop=addressCountry]::text").extract_first()
            
            # print(address)
            

            details = {'Source': 'https://www.construction.co.uk/', 'Firm': firm, 'URL': url, 'Email Address': email_, 'Address Line 1': address_1,
            'State Or County': address_2, 'Country': address_3}


            print(details)

      
            mycol.insert_one(details)

        except Exception as e:
            print(e)

        
        return

    
    
    

       
    
    
   



