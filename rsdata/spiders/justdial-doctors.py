import scrapy
from rsdata.items import Item
import re
from rsdata.cities import cities_list


class JustDialDoctors(scrapy.Spider):
    name = "justdial-doctors"
    cities1 = ["Ahmedabad", "Bangalore", 
      "Chandigarh", "Chennai", "Coimbatore", 
      "Delhi", "Goa", "Gurgaon", "Hyderabad", "Jaipur", "Kolkata", "Mumbai", 
      "Noida", "Pune"
    ]

    cities = cities1 + cities_list

    start_urls = [
      'https://www.justdial.com/'+i+'/57/Doctor_fil' for i in cities
    ]
    
    dict1 = {'9d001':'0', '9d002':'1','9d003':'2','9d004':'3','9d005':'4','9d006':'5','9d007':'6','9d008':'7','9d009':'8','9d010':'9','9d011':'+','9d013':')','9d014':'('}
    dict2 = {'icon-ba':'-', 'icon-acb':'0','icon-yz':'1','icon-wx':'2','icon-vu':'3','icon-ts':'4','icon-rq':'5','icon-po':'6','icon-nm':'7','icon-lk':'8','icon-ji':'9','icon-dc':'+','icon-hg':')','icon-fe':'('}

    def extract_with_css(self, response, query):
        return response.css(query).extract_first()

    def parse(self, response):
        
        city = response.url.replace("https://www.justdial.com/", "").split("/")[0]
        if city not in self.cities:
            return

        for href in response.css('.mm-listview li a::attr("href")'):
            yield response.follow(href, self.parse)

        # follow links to doctor pages
        for dataitem in response.css('.tab-contentphone li.cntanr .store-details'):
            item = Item()
            item["name"] = self.extract_with_css(dataitem, 'h2 a::attr("title")')
            item["url"] = self.extract_with_css(dataitem, 'h2 a::attr("href")')
            area =  self.extract_with_css(dataitem, '.cont_sw_addr::text')
            
            if area is not None and isinstance(area, str):
              item["area"] = re.sub('[^a-zA-Z -_]', '', area)

            item["city"] =  response.css("h1::text").extract_first().split(" ")[-1].strip()
            p = dataitem.css('p.contact-info span').xpath('@class').extract()[1:] 
            item["phone"] = ''.join([self.dict2.get(i.split()[1], 'p') for i in p])
            item["address"] = self.extract_with_css(dataitem, '.cont_fl_addr::text')
            item["sender"] = 'justdial'

            yield item

        # follow pagination links
        for href in response.xpath('//a[@rel="next"]/@href'):
            yield response.follow(href, self.parse)
        