# -*- coding: utf-8 -*-

import datetime


def Now():
    return datetime.datetime.now().strftime('%H:%M:%S.%f')[0:-3] + " "


print Now() + u"正在导入相关模块……"
import arcpy as ap
from urllib2 import urlopen
from bs4 import BeautifulSoup as BS
import time

ap.CheckOutExtension("Spatial")
ap.CheckOutExtension("3D")

T1 = "";
while True:
    try:
        html = urlopen(r"http://www.pm25.com/rank.html", timeout=20)
        # s = html.read()
        print Now() + u"分析网页……"
        soup = BS(html)
        print Now() + u"提取信息……"
        T2 = soup.find("div", {"class": "rank_banner_right"}).find("span").string.encode("utf-8").split('：')[1]
        print Now() + u"更新时间是：", T2,
        if (T2 != T1):
            print Now() + u"   已更新！"
            T1 = T2
            Stations = soup.find("ul", {"class": "pj_area_data_details rrank_box"}).findAll("li")
            dic = {}
            for i in Stations:
                station = i.find("a").contents[0].encode("utf-8")  # .decode("utf-8")
                aqi = i.find("span", {"class": "pjadt_aqi"}).contents[0].encode("utf-8")
                dic[station] = aqi
                # print station, aqi

            print Now() + u"写入信息……"
            ap.env.workspace = "E:/FilesForGIS/Arcpy/AQI/Maps"
            ap.env.extent = "bou2_4p_Project3.shp"
            cursor = ap.da.SearchCursor("AllStations.shp", ["Name", "经度", "纬度"])

            ap.DeleteFeatures_management("NewStations.shp")

            newCursor = ap.da.InsertCursor("NewStations.shp", ["Name", "AQI", "SHAPE@XY"])

            for station in dic:
                cursor.reset()
                for row in cursor:
                    if (station in row[0].encode("utf-8")
                            or (station[-3:] == "\xe5\xb7\x9e"
                                and station[0:-3] in row[0].encode("utf-8"))):
                        newCursor.insertRow((row[0], dic[station], (row[1], row[2])))
                        break

            print Now() + u"删除已有文件……"
            try:
                ap.Delete_management("AQI_Image")
            except:
                print Now() + u"无法删除 AQI_Image"
            try:
                ap.Delete_management("Final_image")
            except:
                print Now() + u"无法删除 Final_image"
            try:
                ap.Delete_management("Extract_AQI_1")
            except:
                print Now() + u"无法删除 Extract_AQI_1"

            print Now() + u"插值计算中……"

            # 克里金插值
            # kModelOrdinary = ap.sa.KrigingModelOrdinary("SPHERICAL")
            # kRadius = ap.sa.RadiusVariable(12)
            # ap.sa.Kriging("NewStations.shp", "AQI", kModelOrdinary, 0.02, kRadius).save("AQI_Image")

            # 反距离权重插值
            searchRadius = ap.sa.RadiusVariable(12)
            ap.sa.Idw("NewStations.shp", "AQI", 0.02, 2, searchRadius).save("AQI_Image")

            print Now() + u"裁剪地图……"
            ebm = ap.sa.ExtractByMask("AQI_Image", "bou2_4p_Project3.shp")
            ebm.save("Final_image")

            print Now() + u"保存地图……"
            mxd = ap.mapping.MapDocument(r"E:\FilesForGIS\Arcpy\AQI\aqiMap2.mxd")
            filename = "aqi_" + time.strftime("%Y%m%d%H%M%S", time.localtime())
            # 离散颜色是第25个，拉伸颜色是第9个
            le = ap.mapping.ListLayoutElements(mxd)[25].text = "更新时间：" + T2 + "  " + str(len(dic))
            ap.mapping.ExportToPNG(mxd, "E:\\FilesForGIS\\Arcpy\\AQI\\outImages\\" + filename)

            print Now(), + u"生成成功！"
        else:
            print Now() + u"未更新"
    except Exception as e:
        print Now(),
        print e
    # break
    time.sleep(100)
