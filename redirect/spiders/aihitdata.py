import scrapy
from scrapy import signals
from scrapy.selector import Selector

from scrapy.http import FormRequest

company_list = []

company_details = []


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""



class QuotesSpider(scrapy.Spider):
    name = "aihitdata"

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print('end')


    def start_requests(self):
        login_url = 'https://www.aihitdata.com/login'
        yield scrapy.FormRequest(login_url,
                            formdata={'csrf_token': 'IjgwODI5ZGQxYjRmMmZlOTg1Y2M3N2YwMjA2NGQ2NWM5MDNjYzBkYWYi.F0Ps5g.OlRsWZDlJpLDl5U22rYpkyP79n0','email': 'biweg62408@glumark.com', 'password': 'ben_zima*1976'},
                            callback=self.start_scraping)
        
    
    def start_scraping(self, response):
        print(response)
        for i in range(1, 101):
            print(f'page: {i}')
            yield scrapy.Request(url=f'https://www.aihitdata.com/search/companies?c=&e=1&i=hospitality+consulting&k=&v=3&l=&p={i}&r=&t=&w=1&rc=', callback=self.parse_two)
        
    def parse_two(self, response):


        links = response.css('div.panel-body > div > a::attr("href")').extract()

        for link in links:
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_three, dont_filter=True)

        
    def parse_three(self, response):
        print(response.page)
        try:
            firm = response.css('h1.text-info::text').extract_first().strip()
            print(firm)
            url = response.css('i.icon-sm.icon-home + a::attr("href")').extract_first()
            print(url)

            # linkedin = response.css('p.url-linkedin a::attr("href")').extract_first()
            # print(url)
        #     address = response.css('span[itemprop=streetAddress]::text').extract_first().strip()

        #     email = response.css('a[itemprop=email]::attr("href")').extract_first()

        #     # print(email)
        #     # phone = response.css('span[itemprop=tel]::text').extract_first()

        #     city = response.css('[itemprop=addressLocality]::text').extract_first().strip()

        #     postal = response.css('[itemprop=postalCode]::text').extract_first().strip()

        #     country = response.css('[itemprop=addressCountry]::text').extract_first().strip()


        #     details = {'Source': 'https://greatnonprofits.org/', 'Firm': firm, 'URL': url, 'Country': country, 'Email Address': email,
        #                 'Address Line 1': address, 'City': city, 'Postal Code': postal}

        #     print(details)
        #     company_details.append(details)           

        #     print(len(company_details))

        #     company_details.append(details)

        except Exception as e:
            print(f'{e}')


