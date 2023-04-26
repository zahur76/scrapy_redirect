import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.gladiatorbusiness.co.uk/all-categories']

class QuotesSpider(scrapy.Spider):
    name = "gladiator"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/gladiator.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.leftCol p a::attr("href")').extract()

        # print(len(links))
        for link in links:
            # print(link)          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'category': link.split('/')[-1]})


    def parse_three(self, response): 
        
        records = response.css('div#recordTotal::text').extract()

        # print(records)
        offset = records[-1].replace('of', '').replace('Businesses', '').replace(',', '').strip()

        for i in range(30, int(offset), 30):
            link = response.url.split('/')[-1]
            mainlink = f'https://www.gladiatorbusiness.co.uk/ajax-active-businesses/{link}?offset={i}'
            yield scrapy.Request(url=response.urljoin(mainlink), callback=self.parse_four, meta={'category': response.meta['category']})

    def parse_four(self, response):

        links = response.css('div.businessItem > a:nth-child(1)::attr("href")').extract()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_five, meta={'category': response.meta['category']})
    

    def parse_five(self, response):
    
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('#websitesWrapper li:nth-of-type(1) a::attr("href")').extract_first()

            email = response.css('p a[href^=mail]::attr("href")').extract_first()

            phone = response.css('p a[href^=tel]::attr("href")').extract_first()

            address_ = response.css('.pageType3 .leftCol p:nth-of-type(1)::text').extract()

            address_= ','.join(address_).strip().replace(',','').replace("\n", "").replace("\r", "")

            details = {'Source': 'https://www.gladiatorbusiness.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Email Address': email,
                     'Address Line 1': address_, 'Business Sector 1': response.meta['category']}

            if email or url:
                print(details)
                company_details.append(details)           

                print(len(company_details))

        except Exception as e:
            print(f'{e}')
