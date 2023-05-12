import scrapy
from scrapy import signals

import pandas as pd
import csv, json

links = pd.read_csv('input/redirect.csv')

redirect_dict = {}


class QuotesSpider(scrapy.Spider):
    name = "redirect"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print(redirect_dict)
        redirect_list = []
        for key, values in redirect_dict.items():
            redirect_list.append(values)
        json_data = json.dumps(redirect_list, ensure_ascii=False)
        json_data = json_data.replace('\\"', "")
        with open(f"output/travelalberta.json", "w", encoding="utf-8") as out:
            out.write(json_data)

    def start_requests(self):
        for int_ in range(len(links)):
            redirect_dict[links.iloc[int_, 0]] = None
        for int_ in range(len(links)):
            yield scrapy.Request(url=links.iloc[int_, 0], callback=self.parse_one,
                                 meta={'input_url': links.iloc[int_, 0], 'download_timeout': 10})

    def parse_one(self, response):
        print(response.meta['input_url'], response.url)

        try:
            redirect_dict[response.meta['input_url']] = response.url
        except:
            redirect_dict[response.meta['input_url']] = None

        # if response.url == None:
        #     yield scrapy.Request(url=redirect_dict[response.meta['input_url']], callback=self.parse_two,  meta={'input_url': response.meta['input_url']})

        return redirect_dict
    
    # def parse_two(self, response):
    #     try:
    #         print(response.meta['input_url'], response.url)
    #         redirect_dict[response.meta['input_url']] = response.url
    #     except:
    #         redirect_dict[response.meta['input_url']] = None

    #     # if response.url == None:
    #     #     yield scrapy.Request(url=redirect_dict[response.meta['input_url']], callback=self.parse_three,  meta={'input_url': response.meta['input_url']})

    #     return redirect_dict
    
    # def parse_three(self, response):
    #     # print(response.meta['input_url'], response.url)
    #     redirect_dict[response.meta['input_url']] = response.url

    #     return redirect_dict



