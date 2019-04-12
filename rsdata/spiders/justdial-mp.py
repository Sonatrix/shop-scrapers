import scrapy
from rsdata.items import Item
import re

class JustDialSpiderMP(scrapy.Spider):
    name = "justdial-mp"
    cities = [
    "Indore","Bhopal","Jabalpur","Gwalior","Ujjain","Sagar","Dewas","Satna","Ratlam","Rewa","Katni","Singrauli","Burhanpur","Khandwa","Bhind","Chhindwara","Guna","Shivpuri","Vidisha","Chhatarpur","Damoh","Mandsaur","Khargone","Neemuch","Hoshangabad","Itarsi","Sehore","Betul","Seoni","Datia","Nagda"
    ]

    start_urls = [
      'https://www.justdial.com/'+i+'/Restaurant-Collections/AllCategory' for i in cities
    ] + [
      'https://www.justdial.com/'+i+'/278/Daily-Needs_fil' for i in cities
    ]
    
    dict1 = {'9d001':'0','9d002':'1','9d003':'2','9d004':'3','9d005':'4','9d006':'5','9d007':'6','9d008':'7','9d009':'8','9d010':'9','9d011':'+','9d013':')','9d014':'('}
    dict2 = {'icon-ba':'-', 'icon-acb':'0','icon-yz':'1','icon-wx':'2','icon-vu':'3','icon-ts':'4','icon-rq':'5','icon-po':'6','icon-nm':'7','icon-lk':'8','icon-ji':'9','icon-dc':'+','icon-hg':')','icon-fe':'('}

    def extract_with_css(self, response, query):
        return response.css(query).extract_first()

    def parse(self, response):
        
        city = response.url.replace("https://www.justdial.com/", "").split("/")[0].strip()
        if city not in self.cities:
            #yield None
            pass

        for href in response.css('.mm-listview li a::attr("href")'):
            yield response.follow(href, self.parse)

        # follow links to author pages
        for dataitem in response.css('.tab-contentphone li.cntanr .store-details'):
            item = Item()
            item["name"] = self.extract_with_css(dataitem, 'h2 a::attr("title")')
            item["url"] = self.extract_with_css(dataitem, 'h2 a::attr("href")')
            item["area"] =  self.extract_with_css(dataitem, '.cont_sw_addr::text').strip()
            item["city"] =  city
            p = dataitem.css('p.contact-info span').xpath('@class').extract()[1:] 
            item["phone"] = ''.join([self.dict2.get(i.split()[1], 'p') for i in p])
            item["address"] = self.extract_with_css(dataitem, '.cont_fl_addr::text')
            item["sender"] = 'justdial-mp'
            #yield response.follow(href, self.parse_data)
            yield item

        # follow pagination links
        for href in response.xpath('//a[@rel="next"]/@href'):
            yield response.follow(href, self.parse)
        