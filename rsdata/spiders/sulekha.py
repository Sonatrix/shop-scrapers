import scrapy
from rsdata.items import Item

class SulekhaSpider(scrapy.Spider):
    name = "sulekha"
    domain = 'https://www.sulekha.com'

    start_urls = ["https://www.sulekha.com/restaurants/all-cities"]
    
    def extract_with_css(self, response, query):
        return response.css(query).extract_first()

    def parse(self, response):
        
        # ity = response.url.replace("https://www.justdial.com/", "").split("/")[0]
        # if city not in cities:
        #     return

        for href in response.css('.citylist li a::attr("href")').extract():
            link_href = self.domain+""+href
            yield response.follow(link_href, self.parse)

        # follow links to author pages
        for dataitem in response.css(".listings li.list-item"):
            item = Item()
            item["name"] = self.extract_with_css(dataitem, 'li::attr("data-name")')
            item["url"] = response.url
            item["area"] =  self.extract_with_css(dataitem, 'li::attr("data-loc")')
            item["city"] =  self.extract_with_css(dataitem, 'li::attr("data-city")')
            item["phone"] = self.extract_with_css(dataitem, 'li::attr("data-bvn")')
            item["address"] = self.extract_with_css(dataitem, 'address::text')
            item["sender"] = 'sulekha'
            #yield response.follow(href, self.parse_data)
            yield item

        # follow pagination links
        for href in response.xpath('//a[@rel="next"]/@href'):
            yield response.follow(href, self.parse)
        