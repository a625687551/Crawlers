import scrapy
import json
from china_wea.items import WeaItem
from scrapy.http import Request
from scrapy.selector import Selector


class Weaspider(scrapy.Spider):
    name = 'china_wea'
    # allow_domain=['tianqi.com']
    start_urls = [
        'http://www.tianqi.com/air/'
    ]

    def parse(self, response):
        # item=WeaItem()
        # tablelist=response.xpath('')
        citylist = response.xpath('//div[@class="meta"]/ul/li')[1:]
        for i in citylist:
            # item['city'] = i.xpath('span[@class="td td-2nd"]/a/text()').extract()[0]
            # item['AQI'] = i.xpath('span[@class="td td-4rd"]/text()').extract()[0]
            city = i.xpath('span[@class="td td-2nd"]/a/text()').extract()[0]
            AQI = i.xpath('span[@class="td td-4rd"]/text()').extract()[0]
            url_2 = 'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=DhzUPOCzgD3zrfRChfombTGZh59v9fGG'
            # print(city,type(city))
            yield Request(url_2.format(city), callback=self.get_address, meta={'city': city, 'AQI': AQI})

    def get_address(self, response):
        item = WeaItem()
        try:
            address = json.loads(response.text)['result']['location']
            item['LNG'] = address['lng']
            item['LAT'] = address['lat']
        except:
            item['LNG'] = None
            item['LAT'] = None
        item['city'] = response.meta['city']
        item['AQI'] = response.meta['AQI']
        yield item

        # body > div.w960.clearfix > div.left614 > div > div.meta > ul
        # print(citylist)

    # def parse(self, response):
    #     item=WeaItem()
    #     item['city']=response.css(u'div.crumbs.fl > a::text').extract()
    #     sevenday=response.xpath('//ul[@class="t clearfix"]')
    #     item['date'] = sevenday.css(u'li.sky> h1::text').extract()
    #     item['clim'] = sevenday.css(u'p.wea::text').extract()
    #     item['temph'] = sevenday.css(u'p.tem span::text').extract()
    #     item['templ'] = sevenday.css(u'p.tem i::text').extract()
    #     item['wind'] = sevenday.css(u'p.win i::text').extract()
    #
    #     yield item
    #     # print(item)
