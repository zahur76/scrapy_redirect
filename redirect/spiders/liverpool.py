import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = [
'https://www.explore-liverpool.com/listings-search-page/page/1/?geodir_search=1&stype=gd_place&spost_category%5B0%5D&s=+&snear&sgeo_lat&sgeo_lon'
]


class QuotesSpider(scrapy.Spider):
    name = "liverpool"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/liverpool.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1, 38):          
            yield scrapy.Request(url=f'https://www.explore-liverpool.com/listings-search-page/page/{i}/?geodir_search=1&stype=gd_place&spost_category%5B0%5D&s=+&snear&sgeo_lat&sgeo_lon', callback=self.parse_two)

    
    def parse_two(self, response):

        # print(response.url)
        
        links = response.css('section.pp-wrapper-link::attr("data-pp-wrapper-link")').extract()

        for link in links:
            link_ = link.replace('{"url":"', '').replace('","is_external":"","nofollow":""}', '').replace('\\','') 
            yield scrapy.Request(url=link_, callback=self.parse_three, meta={'page': response.url})


    def parse_three(self, response):

        try:
            firm = response.css('.elementor-heading-title::text').extract_first()


            email = response.css('.elementor-element-773592e span.elementor-icon-list-text::text').extract_first()

            address  = response.css('.elementor-element-5645975 span.elementor-icon-list-text::text').extract_first()

            phone  = response.css('a:has(i.fa-phone-square-alt) span.elementor-icon-list-text::text').extract_first()

            details = {'Source': 'https://www.explore-liverpool.com/', 'Firm': firm, 'Email Address': email, 'Telephone Number': phone,
                    'Address Line 1': address}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')

       


   
