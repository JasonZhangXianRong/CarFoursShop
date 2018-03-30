#-*-coding:utf-8-*-
"""
This code is utf8
"""
import imp
import json
import urllib2
import os
import sys
from thePath import rootPath
sys.path.append(rootPath + "lib")
from superLogger import Logger

class GQBT(object):
    """
    This is GQBT class
    """
    def __init__(self):
        self.useragent = ("Mozilla/5.0 (Linux; Android 6.0;"
                          " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                          " (KHTML, like Gecko) "
                          "Chrome/60.0.3112.113 Mobile Safari/537.36")
        self.headers = {'User-Agent':self.useragent}
        B = imp.load_source('Directory', rootPath + \
                'script/siteproc/car_4s/lib/Directory.py')
        class_drectory = B.GetDir()
        self.outFile = class_drectory.getDirectory()+"GQBT.json"
        self.loginfo = Logger(rootPath + \
                "temp/debugLog/", "CAR4S")
        
    def getHtml(self, url):
        """
        This function is tio get html from url
        Args:
            url
        Return:
            page code
        """
        try:
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
        This is save file
        """
        fp = open(self.outFile, 'a')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def saveText(self, strbject):
        """
        This is save text
        """
        s = strbject.split("\n")
        for sdata in s:
            fp = open(self.outFile, 'a')
            fp.write(sdata + "\n")
            fp.close()
    
    def getPageItems(self, url):
        """
        This function is to get page items
        Args:
            url
        Return:
            json data
        """
        pageCode = self.getHtml(url) 
        if not pageCode:
            self.loginfo.error('GQBT page is null')
            return
        strpage = pageCode.split("var global_dealers_data =")
        str1 = strpage[1]
        str2 = str1.split("var AllCar_data=")
        str3 = str2[0]
        pageItem = str3[1:len(str3)-4]
        pa = pageItem.replace("},{", "}\n{")
        s = pa.split("\n")
        for sdata in s:
            self.saveText(sdata)
    
    def main_spider(self):
        """
        This is main spider
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the GQBT is doing crawling')
        self.getPageItems("http://www.ghac.cn/js/Official/staticData/p_c_dealers_data.js")
        self.loginfo.debug('the GQBT is doing ending')


if __name__ == '__main__':
    spider = GQBT()
    spider.main_spider()














        
        

    

