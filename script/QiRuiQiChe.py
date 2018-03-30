#-*-coding:utf-8-*-
"""
This is utf8 code
"""
import imp
import json
import urllib2
import urllib
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class QRQC(object):
    """
    This class is QRQC 
    """
    def __init__(self):
        self.useragent=(
                "Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36"
                )
        self.headers={'User-Agent':self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory() + "QRQC.json"
        self.loginfo = Logger(rootPath + \
                "temp/debugLog/", "CAR4S")
        
    def getProvinceIdList(self):
        """
        This function uis to get po
        """
        try:
            url = "http://www.chery.cn/Umbraco/Surface/ajax/GetProvinces"
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            jsonPage = json.loads(pageCode)
            return jsonPage
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def getCityIdList(self, provinceId):
        """
        This function is to get city list
        """
        try:
            url = ("http://www.chery.cn/Umbraco/Surface/ajax/GetCitysByProvinceId")
            values_getCounty = {}
            values_getCounty['provinceid'] = provinceId
            data_getCounty = urllib.urlencode(values_getCounty)
            request = urllib2.Request(url, data = data_getCounty, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            jsonPage = json.loads(pageCode)
            return jsonPage
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e.reason)
                return None
                
    def getData(self, provinceId, cityId):
        """
        This is to get data
        """
        try:
            url = ("http://www.chery.cn/Umbraco/Surface/ajax/GetDealersAndProvider")
            values_getCounty = {}
            values_getCounty['PROVINCE_ID'] = provinceId
            values_getCounty['CITY_ID'] = cityId
            data_getCounty = urllib.urlencode(values_getCounty)
            request = urllib2.Request(url, data = data_getCounty, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            jsonPage = json.loads(pageCode)
            return jsonPage 
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e.reason)
                return None
                
    def saveFile(self, item):
        """
        This is to save file
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii = False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def main_spider(self):
        """
        This is main spider
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the QRQC is doing crawling')
        provinceHtml = self.getProvinceIdList()
        for province in provinceHtml:
            ProId = province["PROVINCE_ID"].encode("utf8")
            ProName = province["PROVINCE_NAME"].encode("utf8")
            cityHtml = self.getCityIdList(ProId)
            for city in cityHtml:
                CityId = city["CITY_ID"].encode("utf8")
                CityName = city["CITY_NAME"].encode("utf8")
                jsonData = self.getData(ProId, CityId)
                for jsData in jsonData:
                    jsData["province"] = ProName
                    jsData["city"] = CityName
                    shopInfo = json.dumps(jsData)
                    items = json.loads(shopInfo)
                    self.saveFile(items)
        self.loginfo.debug('the QRQC is doing ending')
        

if __name__ == '__main__':
    spider = QRQC()
    spider.main_spider()
