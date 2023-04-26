import scrapy
from scrapy import signals

import pandas as pd
import csv


links = pd.read_csv('input/redirect.csv')

redirect_dict = {}

start_urls = ['https://www.financedirectory.net.au/category/insurance/']

company_list = []

company_details = []

count = []


class QuotesSpider(scrapy.Spider):
    name = "australian"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        keys = company_details[0].keys()
        with open('output/output8.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(company_details)

    def start_requests(self):
        for url_ in start_urls:      
            yield scrapy.Request(url=url_, callback=self.parse_one)

    def parse_one(self, response):

        level_one_links = response.css("div.media-body h4.media-heading a::attr('href')").extract()

        for link in level_one_links:

            yield scrapy.Request(url=link, callback=self.parse_two)
            

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css('div.panel-body h4 a::attr("href")').extract()
        

        for company in company_links:
            print(count.append(company))
            print(f'{len(count)}.....................')
            yield scrapy.Request(url=company, callback=self.parse_four, dont_filter=True)
    
        
        the_href = response.css('li a').extract()

        for href in the_href:           
            if href.split('">')[1] == ' &gt;</a>':
                url_ = href.replace('<a href="', '').replace('"> &gt;</a>', '')
                print(url_)          
                yield scrapy.Request(url=url_, callback=self.parse_two, dont_filter=True)


    def parse_four(self, response):
        # print(f'{response.url}....')
        try:
            company_name = response.css('h1 span::text').extract()[0]
        except:
            company_name = None

        try:
            url_ = response.css("a.list-group-item[itemprop='url']::attr('href')").extract()[0]
        except:
            url_ = None
        try:
            address_line_1 = response.css("span[itemprop='streetAddress']::text").extract()[0].strip()
        except:
            address_line_1 = None
        try:
            city = response.css("span[itemprop='addressRegion']::text").extract()[0]
        except:
            city = None

        try:
            postal_code = response.css("span[itemprop='postalCode']::text").extract()[0]
        except:
            postal_code = None
        try:
            country = response.css("span[itemprop='addressCountry']::text").extract()[0]
        except:
            country = None

        try:
            telephone_number = response.css("span[itemprop='telephone']::text").extract()[0]
        except:
            telephone_number = None


        details = {'Firm': company_name, 'URL': url_, 'Telephone Number': telephone_number, 'Address Line 1': address_line_1, 
                    'City': city, 'Postal Code': postal_code, 'Country': country}

        
        company_details.append(details)
    #     yield scrapy.Request(url=url_, callback=self.parse_five, meta={'details' : details})



    def parse_five(self, response):
        
        print(response.url)
        response.meta['details']['URL'] = response.url
        
        
        company_details.append(response.meta['details'])
        print(len(company_details))
        return

    
    
    

       
    
    
   



