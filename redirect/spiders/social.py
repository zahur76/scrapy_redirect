import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = [
'https://www.thesocialmediadirectory.com/locations'
]


class QuotesSpider(scrapy.Spider):
    name = "social"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/social.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for i in range(1,19):       
            yield scrapy.Request(url=f'https://www.thesocialmediadirectory.com/locations/liverpool-merseyside?sortby=name-desc&page={i}', callback=self.parse_three)

    
    def parse_two(self, response):
        
        links = response.css('#listing-view li a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)


    def parse_three(self, response):

        elements = response.css('div.item-content').extract()

        for element in elements:

            try:
                firm = Selector(text=element).css('.item-title a::text').extract_first()


                state = response.css('.item-sorting-title p::text').extract_first().split('for')[1].strip().replace('.', '')


                phone = Selector(text=element).css('.contact-info li:nth-of-type(2)::text').extract_first()

                address  = Selector(text=element).css('.contact-info li:nth-of-type(1)::text').extract_first()

                address = " ".join(address.split())

                business = Selector(text=element).css('.ctg-name a::text').extract_first().strip()

                url = Selector(text=element).css('.contact-info a::text').extract_first()

                details = {'Source': 'https://www.thesocialmediadirectory.com/', 'Business Sector 1':business, 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                        'State Or County': state}

                print(details)
                company_details.append(details)           

                print(len(company_details))

            except Exception as e:
                print(f'{e}')

        try:
            next = response.css('.listing-box-wrap-layout1 > nav a[aria-label="Next »"]::attr("href")').extract_first()
        except:
            next = None

        if next:
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_three, dont_filter=True)


    def parse_four(self, response):

        print(response.url)    
        try:
            firm = response.css('strong.lead::text').extract_first()

            phone = response.css('dt:contains("Phone") + dd::text').extract_first()

            if phone:
                phone = phone.strip()

            url = response.css('dt:contains("Website") + .col-8 a::attr("href")').extract_first()


            state = response.css('span[data-address-county]::text').extract_first()

            city = response.css('span[data-address-town]::text').extract_first()

            postcode = response.css('span[data-address-postcode]::text').extract_first()

            details = {'Source': 'https://www.hotfrog.co.uk/', 'page': response.meta['page'], 'Firm': firm, 'URL': url, 'Telephone Number': phone,
                     'State Or County': state, 'City': city, 'Postal Code': postcode}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
