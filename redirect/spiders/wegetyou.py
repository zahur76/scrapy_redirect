import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://wegetyoufound.co.uk/search/norwich?page=',
]




class QuotesSpider(scrapy.Spider):
    name = "wegetyou"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/wegetyou.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:
            for i in range(1, 55):         
                yield scrapy.Request(url=f'{link}{i}', callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('a.btn-blue::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })



    def parse_three(self, response): 
        
        # print(response.url)
        try:
            firm = response.css('h2.inline-block::text').extract_first()

            address = response.css('div.text-primary:contains(Our Location)::text').extract_first()

            print(firm, address)

            # url = response.css('a.yxt-website-url::attr("href")').extract_first()

            # details = {'Source': response.url, 'Firm': firm, 'URL': url, 'State Or County': response.meta['response'].replace('.opendi.co.uk/', '').replace('https://', '')}

            # print(details)
            # company_details.append(details)           

            # print(len(company_details))

        except Exception as e:
            print(f'{e}')
