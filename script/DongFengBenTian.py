# -*- coding: UTF-8 -*- 
"""
This code is utf8
"""
import imp
import json
import urllib2
import requests
from bs4 import BeautifulSoup
import urllib
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class DFBT(object):
    """
    this class is DFBT
    """
    def __init__(self):
        self.useragent = (
                "Mozilla/5.0 (Linux; Android 6.0;"\
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"\
                " (KHTML, like Gecko) "\
                "Chrome/60.0.3112.113 Mobile Safari/537.36"\
                )
        self.headers = {'User-Agent': self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory() + "DFBT.json"
        self.ProvinceDict = {}
        self.ProvinceDict['1'] = "安徽"
        self.ProvinceDict['124'] = "北京"
        self.ProvinceDict['145'] = "福建"
        self.ProvinceDict['490'] = "广西"
        self.ProvinceDict['240'] = "甘肃"
        self.ProvinceDict['614'] = "贵州"
        self.ProvinceDict['344'] = "广东"
        self.ProvinceDict['1105'] = "黑龙江"
        self.ProvinceDict['928'] = "河南"
        self.ProvinceDict['751'] = "河北"
        self.ProvinceDict['711'] = "海南"
        self.ProvinceDict['1249'] = "湖北"
        self.ProvinceDict['1369'] = "湖南"
        self.ProvinceDict['1581'] = "江苏"
        self.ProvinceDict['1511'] = "吉林"
        self.ProvinceDict['1700'] = "江西"
        self.ProvinceDict['1810'] = "辽宁"
        self.ProvinceDict['1925'] = "内蒙古"
        self.ProvinceDict['2038'] = "宁夏"
        self.ProvinceDict['2067'] = "青海"
        self.ProvinceDict['2524'] = "上海"
        self.ProvinceDict['2406'] = "陕西"
        self.ProvinceDict['2276'] = "山西"
        self.ProvinceDict['2545'] = "四川"
        self.ProvinceDict['2119'] = "山东"
        self.ProvinceDict['2745'] = "天津"
        self.ProvinceDict['2765'] = "西藏"
        self.ProvinceDict['2846'] = "新疆"
        self.ProvinceDict['2962'] = "云南"
        self.ProvinceDict['3108'] = "浙江"
        self.ProvinceDict['3210'] = "重庆"
        self.loginfo = Logger("/home/map/workspace/"\
                "zhangxianrong/crawl-brand/temp/debugLog/", "CAR4S") 
        
    def getCityList(self, provinceId):
        """
        This function is to get city from ctiy Id
        Args:
            province Id
        Return:
            province List
        """
        try:
            url = ("http://www.dongfeng-honda.com/index/get_city_bypid/"
                    + provinceId)
            postData = {}
            postData["dealer_type"] = "dot_query"
            postData["ajax"] = "true"
            data_post = urllib.urlencode(postData)
            request = urllib2.Request(url, data_post, self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            soup = BeautifulSoup(pageCode)
            cityList = soup.find_all('option', attrs={'city_id':True})
            clist = []
            for citystr in cityList:
                clist.append(citystr.get_text().encode('utf8'))
            return clist
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def getData(self, provinceNameCode, cityNameCode):
        """
        This function is get data from prvince id an cityId
        Args:
            provinceNameCode and cityNameCode
        Return:
            json data item
        """
        try:
            url = ("http://www.dongfeng-honda.com/dot_query.shtml?"
                    "province=" + provinceNameCode + "&city=" + cityNameCode)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            bsObject = BeautifulSoup(pageCode)
            items = {}
            items["province"] = provinceNameCode
            items["city"] = cityNameCode
            for li in bsObject.find("section", {"class": "stores"}).ul.findAll("li"):
                list = li.findAll('p')
                items["name"] = li.h4.get_text()
                items["address"] = list[0].get_text()
                items["xiaoshou"] = list[1].get_text()
                items["shouhou"] = list[2].get_text()
            return items
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def saveFile(self, item):
        """
        This function is to save file
        Args:
            json item
        Return:
            json file
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii = False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def getPageItems(self, strPage):
        """
        This function is to wash data
        """
        str1 = pageItem[48: len(pageItem) - 2]
        str2 = str1.replace("},{", "}\n{")
        s = str2.split("\n")
        
    def main_spider(self):
        """
        This function is main spider
        """
        self.loginfo.debug('DFBT is doing crawling')
        for keyId, value in self.ProvinceDict.items():
            provinceListCode = value
            cityList =  self.getCityList(str(keyId))
            for city in cityList:
                if city is not None:
                    dataItem = self.getData(provinceListCode, city)
                    JsonData = json.dumps(dataItem)
                    shopInfo = json.loads(JsonData)
                    self.saveFile(shopInfo)
        self.loginfo.debug('DFBT is doing endding')
        
             
if __name__ == '__main__':
    spider = DFBT()
    spider.main_spider()








            
