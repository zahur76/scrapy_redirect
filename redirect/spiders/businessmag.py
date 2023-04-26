import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import json


company_list = []

company_details = []

links = ['https://www.businessmagnet.co.uk/company/a',
'https://www.businessmagnet.co.uk/town/manchester',
'https://www.businessmagnet.co.uk/town/cambridge',
'https://www.businessmagnet.co.uk/town/norwich',
'https://www.businessmagnet.co.uk/town/peterborough',
'https://www.businessmagnet.co.uk/town/bedford',
'https://www.businessmagnet.co.uk/town/colchester',
'https://www.businessmagnet.co.uk/town/ipswich',
'https://www.businessmagnet.co.uk/town/luton',
'https://www.businessmagnet.co.uk/town/plymouth',
'https://www.businessmagnet.co.uk/town/watford',
'https://www.businessmagnet.co.uk/town/exeter',
'https://www.businessmagnet.co.uk/town/burystedmunds',
'https://www.businessmagnet.co.uk/town/chelmsford',
'https://www.businessmagnet.co.uk/town/hemelhempstead',
'https://www.businessmagnet.co.uk/town/huntingdon',
'https://www.businessmagnet.co.uk/town/stalbans',
'https://www.businessmagnet.co.uk/town/basildon',
'https://www.businessmagnet.co.uk/town/harlow',
'https://www.businessmagnet.co.uk/town/hitchin',
'https://www.businessmagnet.co.uk/town/stevenage',
'https://www.businessmagnet.co.uk/town/greatyarmouth',
'https://www.businessmagnet.co.uk/town/hertford',
'https://www.businessmagnet.co.uk/town/leightonbuzzard',
'https://www.businessmagnet.co.uk/town/welwyngardencity',
'https://www.businessmagnet.co.uk/town/braintree',
'https://www.businessmagnet.co.uk/town/brentwood',
'https://www.businessmagnet.co.uk/town/ely',
'https://www.businessmagnet.co.uk/town/haverhill',
'https://www.businessmagnet.co.uk/town/letchworth',
'https://www.businessmagnet.co.uk/town/royston.htm',
'https://www.businessmagnet.co.uk/town/southendonsea',
'https://www.businessmagnet.co.uk/town/sudbury',
'https://www.businessmagnet.co.uk/town/ware',
'https://www.businessmagnet.co.uk/town/grays',
'https://www.businessmagnet.co.uk/town/thetford',
'https://www.businessmagnet.co.uk/town/redruth',
'https://www.businessmagnet.co.uk/town/borehamwood',
'https://www.businessmagnet.co.uk/town/clactononsea',
'https://www.businessmagnet.co.uk/town/harpenden',
'https://www.businessmagnet.co.uk/town/hatfield',
'https://www.businessmagnet.co.uk/town/hoddesdon',
'https://www.businessmagnet.co.uk/town/lowestoft',
'https://www.businessmagnet.co.uk/town/newmarket',
'https://www.businessmagnet.co.uk/town/saffronwalden',
'https://www.businessmagnet.co.uk/town/sandy',
'https://www.businessmagnet.co.uk/town/walthamabbey',
'https://www.businessmagnet.co.uk/town/wickford',
'https://www.businessmagnet.co.uk/town/wisbech',
'https://www.businessmagnet.co.uk/town/biggleswade',
'https://www.businessmagnet.co.uk/town/diss',
'https://www.businessmagnet.co.uk/town/witham',
'https://www.businessmagnet.co.uk/town/woodbridge',
'https://www.businessmagnet.co.uk/town/berkhamsted',
'https://www.businessmagnet.co.uk/town/maldon',
'https://www.businessmagnet.co.uk/town/billericay',
'https://www.businessmagnet.co.uk/town/pottersbar',
'https://www.businessmagnet.co.uk/town/rickmansworth',
'https://www.businessmagnet.co.uk/town/stowmarket',
'https://www.businessmagnet.co.uk/town/abbotslangley',
'https://www.businessmagnet.co.uk/town/canveyisland',
'https://www.businessmagnet.co.uk/town/epping',
'https://www.businessmagnet.co.uk/town/felixstowe',
'https://www.businessmagnet.co.uk/town/halstead',
'https://www.businessmagnet.co.uk/town/loughton',
'https://www.businessmagnet.co.uk/town/march',
'https://www.businessmagnet.co.uk/town/shefford',
'https://www.businessmagnet.co.uk/town/wymondham',
'https://www.businessmagnet.co.uk/town/dereham',
'https://www.businessmagnet.co.uk/town/kingslynn',
'https://www.businessmagnet.co.uk/town/rayleigh',
'https://www.businessmagnet.co.uk/town/southockendon',
'https://www.businessmagnet.co.uk/town/tilbury',
'https://www.businessmagnet.co.uk/town/attleborough',
'https://www.businessmagnet.co.uk/town/beccles',
'https://www.businessmagnet.co.uk/town/brandon',
'https://www.businessmagnet.co.uk/town/bushey',
'https://www.businessmagnet.co.uk/town/fakenham',
'https://www.businessmagnet.co.uk/town/manningtree',
'https://www.businessmagnet.co.uk/town/mildenhall',
'https://www.businessmagnet.co.uk/town/northwalsham',
'https://www.businessmagnet.co.uk/town/radlett',
'https://www.businessmagnet.co.uk/town/rochford',
'https://www.businessmagnet.co.uk/town/stansted',
'https://www.businessmagnet.co.uk/town/stanfordlehope',
'https://www.businessmagnet.co.uk/town/broxbourne',
'https://www.businessmagnet.co.uk/town/burnhamoncrouch',
'https://www.businessmagnet.co.uk/town/camborne',
'https://www.businessmagnet.co.uk/town/chatteris',
'https://www.businessmagnet.co.uk/town/cheshunt',
'https://www.businessmagnet.co.uk/town/downhammarket',
'https://www.businessmagnet.co.uk/town/frintononsea',
'https://www.businessmagnet.co.uk/town/greatdunmow',
'https://www.businessmagnet.co.uk/town/halesworth',
'https://www.businessmagnet.co.uk/town/ingatestone',
'https://www.businessmagnet.co.uk/town/arlesey',
'https://www.businessmagnet.co.uk/town/cranfield',
'https://www.businessmagnet.co.uk/town/watton',
'https://www.businessmagnet.co.uk/town/bishopsstortford',
'https://www.businessmagnet.co.uk/town/bungay',
'https://www.businessmagnet.co.uk/town/hadleigh',
'https://www.businessmagnet.co.uk/town/leiston',
'https://www.businessmagnet.co.uk/town/ramsey',
'https://www.businessmagnet.co.uk/town/swaffham']




class QuotesSpider(scrapy.Spider):
    name = "businessmag"
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/businessmagnet.json", "w", encoding="utf-8") as out:
            out.write(json_data)
    
    def start_requests(self):
        for link in links:
            for i in range(1,46):   
                yield scrapy.Request(url=f'{link}/page{i}', callback=self.parse_two)

    
    def parse_two(self, response):
        
        links = response.css('.indexinglist a::attr("href")').extract()

        for link in links:          
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three)



    def parse_three(self, response):        

        # print(response.url)
        try:
            firm = response.css('.companyDes h1::text').extract_first()

            url = response.css('.contactDetails a.website::attr("href")').extract_first().replace("http://", '')

            phone = response.css('a.tel::attr("href")').extract_first()

            address = response.css('.companyDes p::text').extract_first()

            town = response.css('.bredCrumb a:nth-of-type(3)::text').extract()[0]

            details = {'Source': 'https://www.businessmagnet.co.uk/', 'Firm': firm, 'URL': url,
                        'Telephone Number': phone, 'Address Line 1': address, 'State Or County': town}

            print(details)
            company_details.append(details)           

            print(len(company_details))

        except Exception as e:
            print(f'{e}')
