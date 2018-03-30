#-*-coding:utf-8-*-
"""
This is utf8 code
"""
import imp
import json
import urllib2
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class CAFT(object):
    """
    This class is chang an fu te
    """
    def __init__(self):
        self.useragent=(
                "Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36"
                )
        self.headers = {'User-Agent': self.useragent}
        B = imp.load_source('Directory', rootPath + \
            'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.getDir()
        self.outFile = class_drectory.getDirectory() + "CAFT.json"
        self.loginfo = Logger(rootPath + \
                "temp/debugLog/", "CAR4S")
        
    def getProvinceCityList(self):
        """
        This function is get pronvince and city
        Return:
            province list
        """
        try:
            url = ("https://www.ford.com.cn/content/ford/cn/"
                   "zh_cn/configuration/application-and-services-config/"
                   "provinceCityDropDowns.multiFieldDropdown.data")
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            ProvinceCityList = json.loads(pageCode)
            return ProvinceCityList
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def getData(self, PClist):
        """
        This function is to wash data
        Args:
            province list
        Return:
            null
        """
        try:
            for PList in PClist:
                provinceName =  PList["provinceKey"].encode('utf8')
                for CList in PList["cityList"]:
                    CityList =  CList["cityKey"].encode("utf8")
                    Address = provinceName + CityList
                    center = self.getCenter(Address)
                    self.getShopInfo(provinceName, CityList, center)
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
    
    def getShopInfo(self, Pname, CName, center):
        """
        This function is to get shop info
        Args:
            province name, city name, center
        Rerurn:
            null
        """
        url = ("https://yuntuapi.amap.com/datasearch/around?s=rsv3"
                "&key=1891d0f847c0a210a88015fdd4c3bc46&extensions=base"
                "&language=en&enc=utf-8&output=jsonp&sortrule=_distance:1"
                "&keywords=&limit=100&tableid=55adb0c7e4b0a76fce4c8dd6"
                "&radius=35000&callback=jsonp_333&platform=JS&logversion=2.0"
                "&sdkversion=1.3&appname=http://www.ford.com.cn/dealer/"
                "locator?intcmp=hp-return-fd&csid=C0F2C0C7-D2A2-4730-9618-5B2C060C3DDD"
                "&center=" + center + 
                "&filter=AdministrativeArea:" + Pname +
                "%20Locality:" + CName +
                "&callback=jsonp_333&_=1505708831023")
        request = urllib2.Request(url, headers = self.headers)
        response = urllib2.urlopen(request)
        pageCode = response.read()
        str1 = pageCode[10: len(pageCode) - 1]
        jsonObj = json.loads(str1)
        for jsonData in jsonObj["datas"]:
            self.saveFile(jsonData)
            
    def getCenter(self, Address):
        """
        This function is to get center
        Args:
            addsree
        Return:
            center code
        """
        url = ("https://restapi.amap.com/v3/geocode/geo"
               "?key=1891d0f847c0a210a88015fdd4c3bc46&s=rsv3"
               "&callback=jsonp_232&platform=JS&logversion=2.0"
               "&sdkversion=1.3&appname=http://www.ford.com.cn/"
               "dealer/locator?intcmp=hp-return-fd"
               "&csid=D6C889F7-2FF1-4EA5-8D60-494D42872518"
               "&address=" + Address + "&callback=jsonp_232&_=1505707122012")
        request = urllib2.Request(url, headers = self.headers)
        response = urllib2.urlopen(request)
        pageCode = response.read()
        str1 = pageCode[10: len(pageCode)-1]
        jsonObj = json.loads(str1)
        for geoCode in jsonObj["geocodes"]:
            return str(geoCode["location"])

    def saveFile(self, item):
        """
        This function is to savefile
        Args:
            json item
        Return:
            null
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def main_spider(self):
        """
        This is main spider
        """
        self.loginfo.debug('CAFT is crowling')
        PClist = self.getProvinceCityList()
        self.getData(PClist)
        self.loginfo.debug('CAFT is end')


    
    








        









            
        













                
