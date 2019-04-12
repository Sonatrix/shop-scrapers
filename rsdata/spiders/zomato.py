import scrapy
from rsdata.items import Item
import re

class ZomatoSpider(scrapy.Spider):
    name = "zomato"

    start_urls = [
        'https://www.zomato.com/chennai/restaurants?page=1',
        'https://www.zomato.com/bangalore/restaurants?page=1',
        'https://www.zomato.com/mysore/restaurants?page=1',
        'https://www.zomato.com/pune/restaurants?page=1',
        'https://www.zomato.com/mumbai/restaurants?page=1',
        'https://www.zomato.com/hyderabad/restaurants?page=1',
        'https://www.zomato.com/kolkata/restaurants?page=1',
        'https://www.zomato.com/ncr/restaurants?page=1',
    ]
    
    def extract_with_css(self, response, query):
        return response.css(query).extract_first().strip()

    def parse(self, response):

        # follow links to author pages
        for dataitem in response.css('#orig-search-list .search-snippet-card'):
            item = Item()
            item["name"] = self.extract_with_css(dataitem, '.result-title::attr("title")')
            item["url"] = self.extract_with_css(dataitem, '.result-title::attr("href")')
            item["area"] =  self.extract_with_css(dataitem, '.search_result_subzone::text')
            item["city"] =  response.css("h1::text").extract_first().split(" ")[-1].strip()
            item["phone"] = self.extract_with_css(dataitem, 'res-snippet-ph-info::attr("data-phone-no-str")')
            item["address"] = self.extract_with_css(dataitem, '.search-result-address::attr("title")')
            item["sender"] = 'zomato'
            #yield response.follow(href, self.parse_data)
            yield item

        # follow pagination links
        for href in response.css('li.current + li.active a').xpath('@href').extract():
            yield response.follow(href, self.parse)
        