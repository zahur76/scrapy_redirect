import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pandas as pd
import csv


links = pd.read_csv('input/redirect.csv')

redirect_dict = {}

# start_urls = ['https://www.superpages.com/las-vegas-nv/credit-debt-counseling?',
#                 'https://www.superpages.com/new-york-ny/insurance?',
#                 'https://www.superpages.com/las-vegas-nv/accountants-certified-public?',
#                 'https://www.superpages.com/las-vegas-nv/loans?',
#                 'https://www.superpages.com/las-vegas-nv/mortgages?',
#                 'https://www.superpages.com/las-vegas-nv/bookkeeping?',
#                 'https://www.superpages.com/las-vegas-nv/stock-bond-brokers?',
#                 'https://www.superpages.com/las-vegas-nv/financial-planning-consultants?']


start_urls = [
                'https://www.superpages.com'
               ]


company_list = []

company_details = []

count = []


class QuotesSpider(scrapy.Spider):
    name = "superpages_all"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        keys = company_details[0].keys()
        with open('output/brokers.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(company_details)

    def start_requests(self):
        for url_ in start_urls: 
            print(url_)     
            yield scrapy.Request(url=url_, callback=self.parse_one , dont_filter=True)
            

    def parse_one(self, response):
        
        links = response.css("section a::attr('href')").extract()

        required_links = ['/categories/insurance', '/categories/auto-insurance', '/categories/boat-marine-insurance', '/categories/business-commercial-insurance', '/categories/dental-insurance']

        new_links = [link for link in links if link in required_links]
        for url_ in new_links:  
            yield scrapy.Request(url=response.urljoin(url_), callback=self.parse_three , dont_filter=True)

    def parse_three(self, response):

        area_links = response.css("div.expand-area a::attr('href')").extract()

        for link_ in area_links:
            yield scrapy.Request(url=response.urljoin(link_), callback=self.parse_four , dont_filter=True)

    def parse_four(self, response):
        # print(response.url)
        company_element = response.css('div.srp-listing').extract()

        for element in company_element:
            # print(element)
            try:
                firm =  Selector(text=element).css("h2.n a.business-name span::text").extract_first()
            except Exception as e:
                print(e)
                firm = None
            # print(firm)
            try:
                url = Selector(text=element).css("a.weblink-button::attr('href')").extract_first()
            except:
                url = None
            # print(url)
            try:
                phone = Selector(text=element).css("a.phones::attr('href')").extract_first()
            except:
                phone = None
            # print(phone)
            try:
                address = Selector(text=element).css("div.street-address::text").extract_first().strip()
            except:
                address = None
            # print(address)
            

            details = {'Source': 'https://www.superpages.com', 'Firm': firm, 'URL': url, 'Telephone Number': phone, 'Address Line 1': address}


            print(details)

            company_details.append(details)

           
        try:
            next = response.css('a.next.ajax-page::attr("href")').extract()
        except:
            next = None
        
        if next:
            print(next[0])
            yield scrapy.Request(url=response.urljoin(next[0]), callback=self.parse_one, dont_filter=True)
        
        return
        


    # def parse_four(self, response):
    #     # print(f'{response.url}....')
    #     try:
    #         company_name = response.css('h1 span::text').extract()[0]
    #     except:
    #         company_name = None

    #     try:
    #         url_ = response.css("a.list-group-item[itemprop='url']::attr('href')").extract()[0]
    #     except:
    #         url_ = None
    #     try:
    #         address_line_1 = response.css("span[itemprop='streetAddress']::text").extract()[0].strip()
    #     except:
    #         address_line_1 = None
    #     try:
    #         city = response.css("span[itemprop='addressRegion']::text").extract()[0]
    #     except:
    #         city = None

    #     try:
    #         postal_code = response.css("span[itemprop='postalCode']::text").extract()[0]
    #     except:
    #         postal_code = None
    #     try:
    #         country = response.css("span[itemprop='addressCountry']::text").extract()[0]
    #     except:
    #         country = None

    #     try:
    #         telephone_number = response.css("span[itemprop='telephone']::text").extract()[0]
    #     except:
    #         telephone_number = None


    #     details = {'Firm': company_name, 'URL': url_, 'Telephone Number': telephone_number, 'Address Line 1': address_line_1, 
    #                 'City': city, 'Postal Code': postal_code, 'Country': country}

        
    #     company_details.append(details)
    # #     yield scrapy.Request(url=url_, callback=self.parse_five, meta={'details' : details})



    # def parse_five(self, response):
        
    #     print(response.url)
    #     response.meta['details']['URL'] = response.url
        
        
    #     company_details.append(response.meta['details'])
    #     print(len(company_details))
    #     return

    
    
    

       
    
    
   



