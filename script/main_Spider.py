import BeiJingBenChi
import BeijingXianDai
import ChangAnFuTe
import DongFengBenTian
import Dongfengrichan
import Guangqibentian
import QiRuiQiChe
import Shanghaitongyongwuling
import Yiqiaodi
import Yiqidazhong
import Yiqifengtian
import multiprocessing
import threading
import sys
sys.path.append("/home/map/workspace/zhangxianrong/crawl-brand/lib")
from dataFormat import FORMATDATA
from dataCompare import COMPAREDATA
from dataTools import DataTools
import time
import imp
import datetime
from superLogger import Logger

class Car4s:
    def __init__(self):
        self.Car4sInfo = ["BJBC", "BJXD", "CAFT", "DFBT", "DFRC", "GQBT", "QRQC","SHTYWL", "YQDZ","YQFT"]
        self.time = time.strftime("%Y-%m-%d")
        self.dateConfPath = "/home/map/workspace/zhangxianrong/crawl-brand/data/formatData/CAR4S/date.txt"      
        self.loginfo = Logger("/home/map/workspace/zhangxianrong/crawl-brand/temp/debugLog/","CAR4S")
    def runSpider(self):
        print "crawling is running..."
        self.loginfo.info('crawling is running')
        process = []
        func = [BeiJingBenChi.BJBC(),
        BeijingXianDai.BJXD(),
        ChangAnFuTe.CAFT(),
        DongFengBenTian.DFBT(),
        Dongfengrichan.DFRC(),
        Guangqibentian.GQBT(),
        QiRuiQiChe.QRQC(),
        Shanghaitongyongwuling.SHTYWL(),
        Yiqiaodi.YQAD(),
        Yiqidazhong.YQDZ(),
        Yiqifengtian.YQFT(),
        ]
        begin = datetime.datetime.now()
        for fun in func:
            pro = threading.Thread(target = fun.main_spider, args=())
            process.append(pro)
        for t in process:
            t.setDaemon(True) 
            t.start()
        for t in process:
            t.join()
        end = datetime.datetime.now()
        runtime = end - begin
        self.loginfo.info('runtime: " + str(runtime) + "crawl success')
        print "crawl success..."
        
        
    def format(self):
        print "the process is formatting"
        self.loginfo.info('the process is formatting')
        process = []
        outDir = "/home/map/workspace/zhangxianrong/crawl-brand/data/formatData/"
        outBrand = "CAR4S"
        confBrand = "CAR4S"
        # outName, confFileKey.
        initialDataDate = time.strftime("%Y-%m-%d") 
        branch = 0
        mains = FORMATDATA()
        for car4sinfo in self.Car4sInfo:  
            pro = threading.Thread(target = mains.test, args=(outDir, outBrand, car4sinfo, confBrand, initialDataDate, car4sinfo, 0))
            process.append(pro)
        for t in process:
            t.setDaemon(True)
            t.start()
        for t in process:
            t.join()
        print "succes"
        self.loginfo.info('the process is end')
    
    def compare(self, oldFileDate, newFileDate):
        print "the process is running comapre..."
        self.loginfo.info('the process is running comapre')
        Dir = "/home/map/workspace/zhangxianrong/crawl-brand/data/formatData/CAR4S/"
        lgDir = "/home/map/workspace/zhangxianrong/crawl-brand/data/compareData/CAR4S/"
        mains = COMPAREDATA()
        process = []
        for Car4s in self.Car4sInfo:
            oldFile = Dir + oldFileDate + "/" + Car4s + ".format"
            newFile = Dir + newFileDate + "/" + Car4s + ".format"
            lgFileName = "lg_" + Car4s + ".json"
            pro = multiprocessing.Process(target = mains.test, args=(oldFile, newFile, lgDir, lgFileName))
            process.append(pro)
        for t in process:
            t.start()
        for t in process:
            t.join()
        self.loginfo.info('the process is comapre success')
        print "succes"
        
    
    def dataTool(self, oldFileDate, newFileDate):
        print "the process is running split data..."
        self.loginfo.info('the process is running split data')
        process = []
        outDir = "/home/map/workspace/zhangxianrong/crawl-brand/data/compareData/CAR4S/"
        oldAndNewDir = "/home/map/workspace/zhangxianrong/crawl-brand/data/formatData/CAR4S/"
        mains = dataTools()
        for car4s in self.Car4sInfo:
            oldFile = oldAndNewDir + oldFileDate + "/" + car4s + ".format"
            newFile = oldAndNewDir + newFileDate + "/" + car4s + ".format"
            lgFile = outDir + "/lg_" + car4s + ".json"
            deleteoutName = "delete_" + car4s + ".json"
            newoutName = "new_" + car4s + ".json"
            pro = multiprocessing.Process(target = mains.test, args=(outDir, oldFile, newFile, lgFile, deleteoutName, newoutName))
            process.append(pro)
        for t in process:
            t.start()
        for t in process:
            t.join()
        self.loginfo.info('the process is end')
        print "succes"
        
    def mainRun(self):
        oldFileDate = open(self.dateConfPath, "r")
        if oldFileDate:
            oldDate = oldFileDate.readline().replace("\n","").replace("\r", "").replace("\t","")
        oldFileDate.close()
        self.runSpider()
        self.format()
        self.compare(oldDate, self.time)
        self.dataTool(oldDate, self.time)
        updateFile = open(self.dateConfPath, "w")
        if updateFile:
            updateFile.write(self.time)
        updateFile.close()

if __name__ == '__main__':
    Car4s().mainRun()













