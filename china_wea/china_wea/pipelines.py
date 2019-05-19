# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class ChinaWeaPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # try:
        #     print(u'删除旧文件')
        #     os.remove('wea.txt')
        # except:
        #     print(u'原来没有文件')
        with open('wea.txt','a',encoding='utf-8') as f:
            f.write(item['city']+','+item['AQI']+','+str(item['LAT'])+','+str(item['LNG'])+'\n')
        return item


# city = item['city'][0]
# f.write('city:' + str(city) + "\n\n")
# for date, clim, temph, templ, wind in zip(item['date'], item['clim'], item['temph'], item['templ'], item['wind']):
#     f.write('date:' + str(date))
#     f.write(' clim:' + str(clim))
#     f.write(' temp:' + str(templ) + '\\' + str(temph))
#     f.write(' wind:' + str(wind) + '\n\n')