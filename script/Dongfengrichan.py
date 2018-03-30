#-*-coding:utf-8-*-
"""
This file code is utf8
"""
import imp
import json
import urllib2
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class DFRC(object):
    """
    This class is dong feng ben tian 
    """
    def __init__(self):
        self.useragent = (
                "Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36"
                )
        self.headers = {'User-Agent':self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory()+"DFRC.json"
        self.loginfo = Logger("/home/map/workspace/\
                zhangxianrong/crawl-brand/temp/debugLog/", "CAR4S")
        
    def getProvinceIdList(self):
        """
        this function is get id
        """
        try:
            url = "https://www.dongfeng-nissan.com.cn\
                /Ajax/AjaxSupport.ashx?method=Province"
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            str1 = pageCode[1:len(pageCode)-1]
            str2 = str1.replace("},{", "}\n{")
            str3 = str2.split("\n")
            provinceId = []
            for json_obj in str3:
                json_obj1 = json.loads(json_obj)
                pro_Id = str(json_obj1["ItemID"])
                provinceId.append(pro_Id)
            return provinceId
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def getCityIdList(self, provinceId):
        """
        this function is to get city id
        """
        try:
            url = ("https://www.dongfeng-nissan.com.cn/Ajax/AjaxSupport.ashx?method=City"
                    "&ProvinceID=" + provinceId)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            str1 = pageCode[1:len(pageCode)-1]
            str2 = str1.replace("},{", "}\n{")
            str3 = str2.split("\n")
            CityId=[]
            for json_obj in str3:
                json_obj1 = json.loads(json_obj)
                pro_Id = str(json_obj1["Code"])
                CityId.append(pro_Id)
            return CityId
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def getData(self, provinceId, cityId):
        """
        This function is to get finally data
        """
        try:
            url = ("https://www.dongfeng-nissan.com.cn/Ajax/AjaxDealer.ashx?"
                   "method=getdealerbycity&"
                   "cityid=" + cityId + "&"
                   "provinceid=" + provinceId + "&contentpath"
                   "=/sitecore/content/DFLOffical/Nissan/buy/selection/find-dealer")
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            json_obj = json.loads(pageCode)
            data1 = json_obj["data"]
            for dataList in data1:
                self.saveFile(dataList)
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
    
    def saveFile(self, item):
        """
        this function is to save file
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii = False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def getPageItems(self, strPage):
        """
        This function is to get pagr data
        """
        str1 = pageItem[48:len(pageItem) - 2]
        str2 = str1.replace("},{", "}\n{")
        s = str2.split("\n")
        
    def main_spider(self):
        """
        This function is main function
        """
        self.loginfo.debug('the DFRC is doing crawling')
        pro_idlist = self.getProvinceIdList()
        for province in pro_idlist:
            city_idList = self.getCityIdList(province)
            for city in city_idList:
                self.getData(province, city)
        self.loginfo.debug('the DFRC is doing ending')
        







        
        
