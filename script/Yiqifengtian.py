#-*-coding:utf-8-*-
"""
utf8
"""
import imp
import json
import urllib2
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class YQFT(object):
    """
    The class is YQFT
    """
    def __init__(self):
        self.useragent = ("Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36")
        self.headers = {'User-Agent': self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory() + "YQFT.json"
        self.provinceList=[
            "%E5%A4%A9%E6%B4%A5%E5%B8%82",
            "%E5%8C%97%E4%BA%AC%E5%B8%82",
            "%E6%B2%B3%E5%8C%97%E7%9C%81",
            "%E5%B1%B1%E8%A5%BF%E7%9C%81",
            "%E5%86%85%E8%92%99%E5%8F%A4%E8%87%AA%E6%B2%BB%E5%8C%BA",
            "%E8%BE%BD%E5%AE%81%E7%9C%81",
            "%E5%90%89%E6%9E%97%E7%9C%81",
            "%E9%BB%91%E9%BE%99%E6%B1%9F%E7%9C%81",
            "%E4%B8%8A%E6%B5%B7%E5%B8%82",
            "%E6%B1%9F%E8%8B%8F%E7%9C%81",
            "%E6%B5%99%E6%B1%9F%E7%9C%81",
            "%E5%AE%89%E5%BE%BD%E7%9C%81",
            "%E7%A6%8F%E5%BB%BA%E7%9C%81",
            "%E6%B1%9F%E8%A5%BF%E7%9C%81",
            "%E5%B1%B1%E4%B8%9C%E7%9C%81",
            "%E6%B2%B3%E5%8D%97%E7%9C%81",
            "%E6%B9%96%E5%8C%97%E7%9C%81",
            "%E6%B9%96%E5%8D%97%E7%9C%81",
            "%E5%B9%BF%E4%B8%9C%E7%9C%81",
            "%E5%B9%BF%E8%A5%BF%E5%A3%AE%E6%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA",
            "%E6%B5%B7%E5%8D%97%E7%9C%81",
            "%E9%87%8D%E5%BA%86%E5%B8%82",
            "%E5%9B%9B%E5%B7%9D%E7%9C%81",
            "%E8%B4%B5%E5%B7%9E%E7%9C%81",
            "%E4%BA%91%E5%8D%97%E7%9C%81",
            "%E8%A5%BF%E8%97%8F%E8%87%AA%E6%B2%BB%E5%8C%BA",
            "%E9%99%95%E8%A5%BF%E7%9C%81",
            "%E7%94%98%E8%82%83%E7%9C%81",
            "%E6%BE%B3%E9%97%A8%E7%89%B9%E5%8\
                8%AB%E8%A1%8C%E6%94%BF%E5%8C%BA",
            "%E9%A6%99%E6%B8%AF%E7%89%B9%\
                E5%88%AB%E8%A1%8C%E6%94%BF%E5%8C%BA",
            "%E5%8F%B0%E6%B9%BE%E7%9C%81",
            "%E6%96%B0%E7%96%86%E7%BB%B4%E5\
                %90%BE%E5%B0%94%E8%87%AA%E6%B2%BB%E5%8C%BA",
            "%E5%AE%81%E5%A4%8F%E5%9B%9E%E6%97\
                %8F%E8%87%AA%E6%B2%BB%E5%8C%BA",
            "%E9%9D%92%E6%B5%B7%E7%9C%81",
        ]
        self.loginfo = Logger(rootPath + \
                "temp/debugLog/", "CAR4S")
        
    def getHtml(self, provinceId):
        """
        The function is to get html
        """
        try:
            url = "http://www.ftms.com.cn/app/\
                  dealer/city_stro?province=" + provinceId
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def saveFile(self, item):
        """
        The function is to save File
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def saveText(self, strbject):
        """
        save text
        """
        s = strbject.split("\n")
        for sdata in s:
            fp = open(self.outFile, 'a+')
            fp.write(sdata + "\n")
            fp.close()
    
    def getPageItems(self, provinceId):
        """
        get page item
        """
        pageItem = self.getHtml(provinceId)
        if not pageItem:
            self.loginfo.error('the htmlcode is null')
            return
        pageList = json.loads(pageItem)
        for pList in pageList:
            dealerList = pList["dealer"]
            for json_obj in dealerList:
                self.saveFile(json_obj)
    
    def main_spider(self):
        """
        main spider
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the YQFT  is doing crawling')
        for province in self.provinceList:
            self.getPageItems(province)
        self.loginfo.debug('the YQFT is doing ending')
        
        







            





        








            
        





        
