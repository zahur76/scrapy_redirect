import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.yelono.com/browse-business-cities']


class QuotesSpider(scrapy.Spider):
    name = "norfolk"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/norfolk.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 62):          
            yield scrapy.Request(url=f'https://www.norfolkchamber.co.uk/directory/page/{i}/', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.post-card a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response): 
        print(response.url)      
        try:
            firm = response.css('span.post::text').extract_first()

            phone = response.css('#directory_contact_details_wrapper p:nth-of-type(2)::text').extract_first()

            url = response.css('a#web_link::attr("href")').extract_first()

            email = response.css('a#email_link::attr("href")').extract_first()

            address_ = response.css('#directory_contact_details_wrapper p:nth-of-type(1)::text').extract_first()

            details = {'Source': 'https://www.bizify.co.uk/', 'Firm': firm, 'URL': url, 'Email Address': email, 'Telephone Number': phone,
                     'Address Line 1': address_,}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
