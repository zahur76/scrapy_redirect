import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.4ni.co.uk/directory/1/northern-ireland-entertainment',
'https://www.4ni.co.uk/directory/3/northern-ireland-shopping',
'https://www.4ni.co.uk/directory/8/northern-ireland-education',
'https://www.4ni.co.uk/directory/11/northern-ireland-construction',
'https://www.4ni.co.uk/directory/34/northern-ireland-weddings',
'https://www.4ni.co.uk/directory/36/northern-ireland-tradesmen',
'https://www.4ni.co.uk/directory/33/northern-ireland-woman',
'https://www.4ni.co.uk/directory/26/northern-ireland-legal-accountancy',
'https://www.4ni.co.uk/directory/6/northern-ireland-travel-and-tourism',
'https://www.4ni.co.uk/directory/4/northern-ireland-property',
'https://www.4ni.co.uk/directory/21/northern-ireland-wholesalers',
'https://www.4ni.co.uk/directory/31/northern-ireland-business',
'https://www.4ni.co.uk/directory/35/northern-ireland-computing',
'https://www.4ni.co.uk/directory/5/northern-ireland-motoring',
'https://www.4ni.co.uk/directory/18/northern-ireland-health',
'https://www.4ni.co.uk/directory/22/northern-ireland-manufacturing',
'https://www.4ni.co.uk/directory/23/northern-ireland-advertising-media-printing',
'https://www.4ni.co.uk/directory/7/northern-ireland-sport',
'https://www.4ni.co.uk/directory/10/northern-ireland-farming-agriculture',
'https://www.4ni.co.uk/directory/16/northern-ireland-banking-and-finance',
'https://www.4ni.co.uk/directory/24/northern-ireland-engineering',
'https://www.4ni.co.uk/directory/25/northern-ireland-freight-storage-warehousing',
'https://www.4ni.co.uk/directory/14/northern-ireland-homes-garden',
'https://www.4ni.co.uk/directory/20/northern-ireland-food-processes',
]


# links = ['https://www.4ni.co.uk/directory/1/northern-ireland-entertainment']



class QuotesSpider(scrapy.Spider):
    name = "propertyN"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/propertyN.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:            
            yield scrapy.Request(url=link, callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('div.directory-cat-list a::attr("href")').extract()
        
        for link in links:
            if 'thebiglist' in link:   
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_four, meta={'response': response.meta['response'] })
            else:
                yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })


    def parse_three(self, response): 


        links_ = response.css('div.DefaultRoundedCornerBox:nth-of-type(n+2) a::attr("href")').extract()

        for link in links_:        
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_five, meta={'response': response.meta['response'] })

        try:
            next = response.css('a#contentBody_hypNext::attr("href")').extract_first()
        except:
            next = None
        if next:
            # print('next exists')
            yield scrapy.Request(url=response.urljoin(next), callback=self.parse_three, meta={'response': response.meta['response']}, dont_filter=True)


    def parse_four(self, response):

        links__ = response.css('td a::attr("href")').extract()

        for link in links__:        
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_six, meta={'response': response.meta['response'] })


    def parse_five(self, response):
        print(response.url)
        print('na')
        try:
            firm = response.css('h1::text').extract_first().strip()

            phone = response.css("div[itemprop='telephone']::text").extract_first().strip()

            url = response.css('a#cWebsiteLink::attr("href")').extract_first()

            email = response.css('div.listingContactDetails-info a[href^=mailto]::attr("href")').extract_first()

            address_1 = response.css('div[itemprop="streetAddress"]::text').extract_first()

            state = response.css('div[itemprop="addressRegion"]::text').extract_first()

            postal = response.css('div[itemprop="postalCode"]::text').extract_first()

            details = {'Source': 'https://www.4ni.co.uk/', 'Firm': firm, 'Telephone Number': phone, 'URL': url,
                'Email Address': email, 'Address Line 1': address_1, 'State Or County': state, 'Postal Code': postal}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
    

    def parse_six(self, response):
        print('big list')
        try:
            firm = response.css('h1::text').extract_first().strip()

            phone = response.css("tr:contains('Telephone:') td:nth-of-type(2)::text").extract_first().strip()

            url_ = response.css('tr:contains("Website:") td:nth-of-type(2)').extract()

            for a in url_:
                url = Selector(text=a).css('a::text').extract_first()

            # email = response.css('tr:contains("Email:") td:nth-of-type(2)').extract()

            address_1 = response.css('tr:contains("Address:") td:nth-of-type(2)::text').extract_first()

            details = {'Source': 'https://www.4ni.co.uk/', 'Firm': firm, 'Telephone Number': phone, 'URL': url,
                'Email Address': None, 'Address Line 1': address_1}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
