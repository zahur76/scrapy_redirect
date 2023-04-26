import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://cheshunt.opendi.co.uk/',
'https://huntingdon.opendi.co.uk/C/company-directory.html',
'https://bury-st-edmunds.opendi.co.uk/C/company-directory.html',
'https://ely.opendi.co.uk/C/company-directory.html',
'https://grays.opendi.co.uk/C/company-directory.html',
'https://ipswich.opendi.co.uk/C/company-directory.html',
'https://watford.opendi.co.uk/C/company-directory.html',
'https://basildon.opendi.co.uk/C/company-directory.html',
'https://brentwood.opendi.co.uk/C/company-directory.html',
'https://canvey-island.opendi.co.uk/C/company-directory.html',
'https://chelmsford.opendi.co.uk/C/company-directory.html',
'https://great-yarmouth.opendi.co.uk/C/company-directory.html',
'https://harlow.opendi.co.uk/C/company-directory.html',
'https://hemel-hempstead.opendi.co.uk/C/company-directory.html',
'https://leighton-buzzard.opendi.co.uk/C/company-directory.html',
'https://loughton.opendi.co.uk/C/company-directory.html',
'https://lowestoft.opendi.co.uk/C/company-directory.html',
'https://luton.opendi.co.uk/C/company-directory.html',
'https://newmarket.opendi.co.uk/C/company-directory.html',
'https://peterborough.opendi.co.uk/C/company-directory.html',
'https://potters-bar.opendi.co.uk/C/company-directory.html',
'https://region-east.opendi.co.uk/flitwick/',
'https://region-east.opendi.co.uk/letchworth/',
'https://region-east.opendi.co.uk/stotfold/',
'https://st-albans.opendi.co.uk/C/company-directory.html',
'https://stevenage.opendi.co.uk/C/company-directory.html',
'https://stowmarket.opendi.co.uk/C/company-directory.html',
'https://thetford.opendi.co.uk/C/company-directory.html',
'https://waltham-abbey.opendi.co.uk/C/company-directory.html',
'https://wickford.opendi.co.uk/C/company-directory.html',
'https://wisbech.opendi.co.uk/C/company-directory.html',
'https://billericay.opendi.co.uk/C/company-directory.html',
'https://harpenden.opendi.co.uk/C/company-directory.html',
'https://ware.opendi.co.uk/C/company-directory.html',
'https://welwyn-garden-city.opendi.co.uk/C/company-directory.html',
'https://biggleswade.opendi.co.uk/C/company-directory.html',
'https://arlesey.opendi.co.uk/',
'https://braintree.opendi.co.uk/C/company-directory.html',
'https://clacton-on-sea.opendi.co.uk/C/company-directory.html',
'https://colchester-essex.opendi.co.uk/C/company-directory.html',
'https://felixstowe.opendi.co.uk/C/company-directory.html',
'https://haverhill.opendi.co.uk/C/company-directory.html',
'https://hertford.opendi.co.uk/C/company-directory.html',
'https://kings-lynn.opendi.co.uk/C/company-directory.html',
'https://rayleigh.opendi.co.uk/C/company-directory.html',
'https://royston.opendi.co.uk/C/company-directory.html',
'https://royston.opendi.co.uk/C/company-directory.html',
'https://southend-on-sea.opendi.co.uk/C/company-directory.html',
'https://st-neots.opendi.co.uk/C/company-directory.html',
'https://march.opendi.co.uk/C/company-directory.html',
'https://rickmansworth.opendi.co.uk/C/company-directory.html',
'https://bedford.opendi.co.uk/C/company-directory.html',
'https://berkhamsted.opendi.co.uk/C/company-directory.html',
'https://maldon.opendi.co.uk/C/company-directory.html',
'https://region-east.opendi.co.uk/whittlesey/',
'https://rochford.opendi.co.uk/C/company-directory.html',
'https://sandy.opendi.co.uk/C/company-directory.html',
'https://stanford-le-hope.opendi.co.uk/C/company-directory.html',
'https://bushey.opendi.co.uk/C/company-directory.html',
'https://harwich.opendi.co.uk/C/company-directory.html',
'https://hoddesdon.opendi.co.uk/C/company-directory.html',
'https://south-ockendon.opendi.co.uk/C/company-directory.html',
'https://witham.opendi.co.uk/C/company-directory.html',
'https://shefford.opendi.co.uk/C/company-directory.html',
]




class QuotesSpider(scrapy.Spider):
    name = "opendi"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/opendi.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:            
            yield scrapy.Request(url=link, callback=self.parse_two, meta={'response': link})

    
    def parse_two(self, response):
        
        links = response.css('button[class^=js-link]::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, meta={'response': response.meta['response'] })



    def parse_three(self, response): 
   
        try:
            firm = response.css('h1::text').extract_first()

            url = response.css('a.yxt-website-url::attr("href")').extract_first()

            details = {'Source': response.url, 'Firm': firm, 'URL': url, 'State Or County': response.meta['response'].replace('.opendi.co.uk/', '').replace('https://', '')}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
