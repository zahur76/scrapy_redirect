import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.gladiatorbusiness.co.uk/all-categories']

class QuotesSpider(scrapy.Spider):
    name = "gladiator3"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/gladiator3.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(30, 11900, 15):
            mainlink = f'https://www.gladiatorbusiness.co.uk/ajax-active-businesses/liverpool?offset={i}'
            yield scrapy.Request(url=mainlink, callback=self.parse_four)


    def parse_four(self, response):
        print(response.url)
        links = response.css('div.businessItem > a:nth-child(1)::attr("href")').extract()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_five)
    

    def parse_five(self, response):
        print(response.url)
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('#websitesWrapper li:nth-of-type(1) a::attr("href")').extract_first()

            email = response.css('p a[href^=mail]::attr("href")').extract_first()

            phone = response.css('p a[href^=tel]::attr("href")').extract_first()

            address_ = response.css('.pageType3 .leftCol p:nth-of-type(1)::text').extract()

            address_= ','.join(address_).strip().replace(',','').replace("\n", "").replace("\r", "")

            details = {'Source': 'https://www.gladiatorbusiness.co.uk/', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Email Address': email,
                     'Address Line 1': address_}

            print(details)
            if email or url:
                
                company_details.append(details)           

                print(len(company_details))

        except Exception as e:
            print(f'{e}')
