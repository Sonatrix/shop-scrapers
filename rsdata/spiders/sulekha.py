import scrapy
from rsdata.items import Item

class SulekhaSpider(scrapy.Spider):
    name = "sulekha"
    domain = 'https://www.sulekha.com'
    page_id = 'eyIkaWQiOiIxIiwiQ2l0eUlkIjo1LCJBcmVhSWQiOjAsIkNhdGVnb3J5SWQiOjMwMywiTmVlZElkIjowLCJOZWVkRmlsdGVyVmFsdWVzIjoiIiwiUm91dGVOYW1lIjoiUmVzdGF1cmFudHMiLCJQYWdlVmlld1R5cGUiOjQsIkhhc0xjZiI6dHJ1ZSwiQnJlYWRDcnVtYlRpdGxlIjoiUmVzdGF1cmFudHMiLCJJc09ubHlQcmltYXJ5VGFnIjpmYWxzZSwiQ2xlYXJDYWNoZSI6ZmFsc2UsIkh1YklkIjoiIiwiQXR0cmlidXRlcyI6IjAiLCJWZXJzaW9uIjoyLCJJc0FkTGlzdGluZ1BhZ2UiOmZhbHNlLCJJc0FkRGV0YWlsUGFnZSI6ZmFsc2UsIlJlZk5lZWRJZCI6MCwiVGVtcGxhdGVOYW1lIjoiIiwiSXNQd2EiOmZhbHNlfQ%3D%3D'
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
        for dataitem in response.css("li.list-item"):
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
        
        list_num  = self.extract_with_css(response, "#hdnListingPageNumber::attr('value')")
        isNextExists = self.extract_with_css(response, "#hdnBizHasMoreResults::attr('value')")

        if isNextExists == 'True':
            temp = response.url
            new_url = temp.replace("PageNr","old")+'PageNr='+str(int(list_num)+1)
            yield response.follow(new_url, self.parse)

        hasMore =self.extract_with_css(response, "#morebusinesslist .loadlist::text")        #follow pagination links
        if hasMore is not None and "More" in hasMore:
            headCount = int(self.extract_with_css(response, "#hdnBusinessCount::attr('value')"))
            city_name  = self.extract_with_css(response, "#hdnCityName::attr('value')")
            key  = self.extract_with_css(response, "#partialPageData::attr('value')")
            CategoryName  = self.extract_with_css(response, "#hdnCategoryName::attr('value')")
            CategoryId  = self.extract_with_css(response, "#hdnCategoryId::attr('value')")

            PageNr = int(list_num)+1 if list_num is not None else  2
            href = 'https://www.sulekha.com/mvc5/lazy/v1/Listing/get-business-list?PartialPageData='+key+'&Category='+CategoryId+'&PageNr='+str(PageNr)+'&CategoryName='+CategoryName+'&CityName='+city_name
            yield response.follow(href, self.parse)
        