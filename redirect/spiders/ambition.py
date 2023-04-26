import scrapy
from scrapy import signals
from scrapy.selector import Selector
from bs4 import BeautifulSoup as BS
import requests

import pandas as pd
import csv
import json , time
import cloudscraper


links = pd.read_csv('input/redirect.csv')

redirect_dict = {}

start_urls = [
                'https://www.europages.co.uk/companies/medical%20equipment.html'
               ]


# start_urls = [
           
#                 'https://www.europages.co.uk/companies/advertising%20agencies.html'
                
#                ]


company_list = []

company_details = []

count = []

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


class QuotesSpider(scrapy.Spider):
    name = "ambition"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        json_data = json.dumps(company_details, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/ambition.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for i in range(1, 337):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.ambitionbox.com/list-of-companies?IndustryName=biotechnology,healthcare-or-pharma,biotech-and-life-sciences,pharma&sort_by=popularity&page={i}', callback=self.parse_two)


    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".left > a::attr('href')").extract()

        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        print(response.url)

        headers = {
            'authority': 'www.ambitionbox.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            # 'cookie': '_t_ds=e87005c1675936045-16e87005c-0e87005c; _gid=GA1.2.1252494351.1675936048; ak_bmsc=ACAEE9E18C2547E7DEB8D844982810E0~000000000000000000000000000000~YAAQsNPerWn5CiiGAQAAh6KSNRJPHZ2piyGsHz7nGa0SoAZZMIPKWedk/O+NrJIl1KkEYG+CXPu2lpIDY+W1BySubWaYaiO9JypJxyKpALx5aLsKB4MAIFk4wT03J2bX5RCJQd3tDgCWj/d3bp05czK1P6GPenwyExMLXotW+/n3D/tugDMRPiQ2idKVfZSv0WkwZ2l6+bR/RiOwi9ahoPGIpVpnYQL5Iqigw0Gd2U7tECSCBiWUGeH3nweww1wSake+fojgbRvVFxa8Nabh1BeDhrxydyov1OOYBMXlQtxTr6advG0F+woqKk92KpZDNZWzI+YS7K759xTcbghbPksqupCsM0TuZu9k54fePPsL/UQunTorC54DQXF4SoVXrz7RQw87qgBxVEsyfjdBVrgKK2qXeJWItmGiJvIYkOor7paOZWbytKaWPofYHdaP1kWOLfdX6S3OviFWYbR+mcBWFCTE/MGKJCWwajt/EnIX55jFCnnO+bFsxvMfaQ==; _ga=GA1.1.1732713202.1675936048; _ga_HV7DJVVBCW=GS1.1.1675941563.2.1.1675941783.0.0.0; bm_sv=880B812013A39EF3C62627197FBF48B9~YAAQke1lXwWpLCiGAQAAYifqNRJqX5UiiBjFBwY9fd0P6zGOVBVrB6CgC7M5u88RnH0Wn0Do/Rjla2Wvy0lqlee/FCEfMWV8ZvZMKWXxmUH4RytX++AyQaQRoDsPw9dtJyyVzmLUVDIOsD6sywtgZ6A1CxI5bRuNO5jprKs/0Z/qCdUP+ES3WirRJvdytVjgjWxIm5WhH48MDajjU54DBE7VMB7nDxSrO3GYUNZxs9Xw+7AxoeSD4HHQHsNUOS+H/clQTD3nFg==~1',
            'if-none-match': '"60557-Q0J0mDrCC9njtWe8ETneTs0zEb0"',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        scraper = cloudscraper.create_scraper() 

        soup_ = scraper.get(response.url)

        soup = BS(soup_.text, 'lxml')
        # print('za')
        print(soup)

        url = soup_.select_one('.aboutItem__link a').get('href')

        print(url)



        # firm =  response.css("h1::text").extract_first()       
    
        # url = response.css(".aboutItem__link a::text").extract()

        # address = response.css("li:nth-of-type(5) a.aboutItem__link::text").extract_first().strip()
       
        # sector = response.css("li:nth-of-type(1) div.textItem__val:nth-of-type(1) a::text").extract_first().strip()

        # details = {'Source': 'https://www.ambitionbox.com/', 'Firm': firm.strip(), 'URL': url, 'Address Line 1': address,
        # 'Business Sector 1': sector}

        # print(details)

        # company_details.append(details)

        # print(len(company_details))
        
        return

    

       
    
    
   



