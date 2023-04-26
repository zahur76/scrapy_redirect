import scrapy
from scrapy import signals
from scrapy.selector import Selector

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["myhotel"]

mycol = mydb["myhotel"]


class QuotesSpider(scrapy.Spider):
    name = "myhotel"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')
        # json_data = json.dumps(company_details, ensure_ascii=False)
        # json_data = json_data.replace('\\"', "")
        # with open(f"output/europages_pharmaceutical.json", "w", encoding="utf-8") as out:
        #     out.write(json_data)

    def start_requests(self):
        for i in range(1, 165):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://myhotel.giatamedia.com/hotel-directory?page={i}', callback=self.parse_two)
        

    def parse_two(self, response):
        # print(response.url)
        company_links = response.css(".col-xs-25 a::attr('href')").extract()   


        for company in company_links:
            yield scrapy.Request(url=response.urljoin(company), callback=self.parse_three , dont_filter=True)
    

    def parse_three(self, response):
        print(response.url)
        try:
            firm =  response.css("h1#title::text").extract_first()
        except Exception as e:
            print(e)
            firm = None
        # print(firm)
        try:
            url = response.xpath("//*[@id='property-container']/div[5]/div/div/div/div[2]/div[2]/div/span/text()[3]").extract_first()
        except:
            url = None
        
        if url == 'https:/':
            url = response.xpath('//*[@id="property-container"]/div[5]/div/div/div/div[2]/div/div/span/text()[3]').extract_first()

        if not url:
            url = response.xpath('//*[@id="property-container"]/div[5]/div/div/div/div[2]/div/div/span/text()[3]').extract_first()
        try:
            email = response.xpath("//*[@id='property-container']/div[5]/div/div/div/div[2]/div[1]/div/span/text()").extract_first()
        except:
            email = None
        
        if not '@' in email:
            email = None
        
        try:
            phone = response.xpath("//*[@id='property-container']/div[5]/div/div/div/div[1]/div[2]/div/span/text()").extract_first()
        except:
            phone = None

        try:
            address = response.css("p.location::text").extract()[1].strip()
        except:
            address = None
                

        details = {'Source': 'https://myhotel.giatamedia.com/', 'Firm': firm.strip(), 'URL': url, 'Email Address': email, 'Telephone Number': phone, 'Address Line 1': address}

        print(details)

        mycol.insert_one(details)
        
        return

   



