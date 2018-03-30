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

class YQDZ(object):
    """
    This class is YQAD
    """
    def __init__(self):
        self.url = "http://contact.faw-vw.com/uploadfiles/js/dealer.js"
        self.useragent = ("Mozilla/5.0 (Linux; Android 6.0;"
                          " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                          " (KHTML, like Gecko) "
                          "Chrome/60.0.3112.113 Mobile Safari/537.36")
        self.headers = {'User-Agent': self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'crawl-brand/script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory() + "YQDZ.json"
        self.loginfo = Logger(rootPath + "temp/debugLog/", "CAR4S")
        
    def getHtml(self):
        """
        This function is get html
        """
        try:
            request = urllib2.Request(self.url, headers = self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError as e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def saveFile(self, item):
        """
        This function is to save file
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()

    def getPageItems(self):
        """
        This function is to get page code
        """
        pageItem = self.getHtml()
        if not pageItem:
            self.loginfo.error('YQDZ is null')
        str1 = pageItem[17:len(pageItem) - 1]
        str2 = str1.replace("},{", "}\n{")
        s = str2.split("\n")
        for sdata in s:
            json_get_rpid = json.loads(sdata)
            items = {}
            items["city"] = json_get_rpid["vc_name"]
            items["tel"] = json_get_rpid["vd_salePhone"]
            items["name"] = json_get_rpid["vd_dealerName"]
            items["longitude"] = json_get_rpid["vd_longitude"]
            items["latitude"] = json_get_rpid["vd_latitude"]
            items["address"] = json_get_rpid["vd_address"]
            items["province"] = json_get_rpid["vp_name"]
            self.saveFile(items)
    
    def main_spider(self):
        """
        This is main spider
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the YQDZ is doing crawling')
        self.getPageItems()
        self.loginfo.debug('the YQDZ is doing ending')


































# B =imp.load_source('Directory','D:/Project/car_4s/bin/Directory.py')
# outFile=B.getDirectory()+"Yiqidazhong.json"
# url = ("http://contact.faw-vw.com/uploadfiles/js/dealer.js")
# request_city = urllib2.Request(url)
# response_city = urllib2.urlopen(request_city)
# html_city = response_city.read()
# str1 = html_city[17:len(html_city) - 1]
# str2=str1.replace("},{","}\n{")
# s=str2.split("\n")
# for sdata in s:



