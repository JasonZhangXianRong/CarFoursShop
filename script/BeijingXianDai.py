#-*-coding:utf-8-*-
"""
Beijing xiandai 
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
class BJXD(object):
    """
    This class is BJXD
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
        self.outFile = class_drectory.getDirectory() + "BJXD.json"
        self.loginfo = Logger(rootPath + "temp/debugLog/", "CAR4S")
        
    def getData(self):
        """
        This is to get data
        """
        try:
            url = ("https://www.beijing-hyundai.com.cn/\
                    datacenter/static/js/District.js")
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                self.loginfo.error('correct', e.reason)
                
    def saveFile(self, item):
        """
        This is to save file
        """
        fp = open(self.outFile, 'a+')
        fp.write(item)
        fp.close()
    
    def getPageItems(self, strPage):
        """
        This is to get page items
        """
        str1 = pageItem[48:len(pageItem) - 2]
        str2 = str1.replace("},{", "}\n{")
        s = str2.split("\n")
        
    def main_spider(self):
        """
        This is main spider
        """
        self.loginfo.debug('BJXD is crawl')
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        htmlcode = self.getData()
        if htmlcode:
            htmlcode1 = re.findall(r"{(.+?)}", htmlcode)
            for data in htmlcode1:
                data = data.replace(" ", "").replace("\n","").replace("\t","").replace("\r","")
                data = "{" + data + "}"
                data = json.loads(data)
                data = json.dumps(data, ensure_ascii = False) + "\n"
                self.saveFile(data.encode("utf8"))
        self.loginfo.debug('BJXD is end')


if __name__ == '__main__':
    BJXD().main_spider()


        










                
        
