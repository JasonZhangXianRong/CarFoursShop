#-*-coding:utf-8-*-
"""
This file coding utf8
"""
import imp
import json
import urllib2
import os
import re
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class YQAD(object):
    """
    This class is yiqiaodi spider
    """
    def __init__(self):
        self.useragent=("Mozilla/5.0 (Linux; Android 6.0;"
                        " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                        " (KHTML, like Gecko) "
                        "Chrome/60.0.3112.113 Mobile Safari/537.36")
        self.headers={'User-Agent':self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory() + "YQAD.json"
        self.loginfo = Logger(rootPath + "/temp/debugLog/", "CAR4S")
        
    def getHtml(self):
        """
        This function is to get html code
        """
        try:
            url = "http://contact.audi.cn/dictionary_js/map_dealer.js"
            request = urllib2.Request(url, headers=self.headers)
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
    
    def saveText(self, strbject):
        """
        This is to save text file
        """
        s = strbject.split("\n")
        for sdata in s:
            fp = open(self.outFile, 'a+')
            fp.write(sdata + "\n")
            fp.close()

    def getPageItems(self):
        """
        This function is to wash data
        """
        pageItem = self.getHtml()
        if not pageItem:
            self.loginfo.error('YQAD page is null')
        str1 = pageItem[48: len(pageItem) - 2]
        str2 = str1.replace("},{", "}\n{")
        s = str2.split("\n")
        for sdata in s:
            json_get_rpid = json.loads(sdata)
            items = {}
            items["company"] = json_get_rpid["company"]
            items["address"] = json_get_rpid["address"]
            items["point"] = json_get_rpid["point"]
            items["tel"] = json_get_rpid["tel"]
            self.saveFile(items)
    
    def main_spider(self):
        """
        This function is main function
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the YQAD is doing crawling')
        pageCode = self.getHtml()
        str1=str(pageCode).split("type")
        str2 = str1[1]
        str3 = str2[4:]
        self.saveText(str3)       
        self.loginfo.debug('the YQAD is doing ending')


if __name__ == '__main__':
    YQAD().main_spider()




