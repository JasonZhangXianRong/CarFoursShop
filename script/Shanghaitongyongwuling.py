#-*-coding:utf-8-*-
"""
utf8
"""
import imp
import json
import urllib2
import sys
from thePath import rootPath
sys.path.append(rootPath + "tools/geo-client-py")
import geocoding
import os
import sys
sys.path.append(rootPath + "lib")
from superLogger import Logger
class SHTYWL(object):
    """
    This is shang hai tongyong wuling
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
        outFile = class_drectory.getDirectory() + "SHTYWL.json"
        self.outFile = outFile
        self.loginfo = Logger(rootPath + \
                "temp/debugLog/", "CAR4S")
        
    def getHtml(self, pageIndex):
        """
        This is get html
        """
        try:
            url = "http://www.sgmw.com.cn/ashx/dealerInfo.ashx?\
                   r=0.8773350179008588&city=" + str(pageIndex)
            url2 = "http://www.sgmw.com.cn/js/dealer_data.js?v=0.5240752546493617"
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
        fp = open(self.outFile, 'a+')
        li = json.dumps(item, ensure_ascii = False) + '\n'
        fp.write(li.encode('utf8'))
        fp.close()

    def getPageItems(self, pageIndexs):
        """
        The function is to get page code
        """
        pageItem = self.getHtml(pageIndex = pageIndexs)
        if not pageItem:
            self.loginfo.error('SHTYWL page is null')
        str1 = pageItem[48:len(pageItem) - 2]
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
    
    def getcity(self, address, admin):
        """
        The function is to get city
        """
        addr = address.decode("utf8").encode("gbk")
        adm = admin.decode("utf8").encode("gbk")
        line = addr + '@' + adm
        addrInfo = geocoding.test(addr, adm, line, 1)
        if "result" in addrInfo:
            str1 = addrInfo["result"][0]["formatted_address"]
            return str1
            
    def main_spider(self):
        """
        This is main
        """
        if os.path.exists(self.outFile):
            os.system("rm " + self.outFile)
        self.loginfo.debug('the SHTYWL is doing crawling')
        for cityid in range(0, 27):
            self.getPageItems(cityid)
        self.loginfo.debug('the SHTYWL is doing ending')
        

if __name__ == '__main__':
    spider = SHTYWL()
    spider.main_spider()


