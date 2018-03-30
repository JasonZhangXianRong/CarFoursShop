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

class BJBC(object):
    """
    BJBC class
    """
    def __init__(self):
        self.useragent = (
                "Mozilla/5.0 (Linux; Android 6.0;"
                " Nexus 5 Build/MRA58N) AppleWebKit/537.36"
                " (KHTML, like Gecko) "
                "Chrome/60.0.3112.113 Mobile Safari/537.36"
                )
        self.headers={'User-Agent':self.useragent}
        B = imp.load_source('Directory', rootPath +\
                'script/siteproc/car_4s/lib/Directory.py')
        self.class_drectory = B.GetDir()
        self.outFile = self.class_drectory.getDirectory() + "BJBC.json"
        self.loginfo = Logger(rootPath + "temp/debugLog/", "CAR4S")
        
    def getData(self,provinceId):
        """
        Get Data
        """
        try:
            url = ("http://dealer.mercedes-benz.com.cn/dealers/index.php?"
                   "option=com_car_dealers&task=dealers.getDealers"
                   "&pid=" + provinceId + "&cid=0&callback=jsonpCallback"
                   "&callback=jsonpCallback&_=1505449207501"
                  )
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                self.loginfo.error(e)
                return None
                
    def saveFile(self, item):
        """
        This function is to saveFile
        """
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii=False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()
    
    def getPageItems(self, strPage):
        """
        This is to get page item
        """
        str1 = strPage[14:len(strPage) - 1]
        htmlJsonData =json.loads(str1)
        jsonDataList = htmlJsonData["data"]["dealer"]
        for jsonData in jsonDataList:
            self.saveFile(jsonData)
    
    def main_spider(self):
        """
        This is main spider
        """
        self.loginfo.debug('BJBC is crowling')
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        for pid in range(1,32):
            htmlCode = self.getData(str(pid))
            if htmlCode:
                self.getPageItems(htmlCode)
        self.loginfo.debug('BJBC is end')
    

if __name__ == '__main__':
    BJBC()



    
    
