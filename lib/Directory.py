"""
This is to get directory
"""
import time
import os
from thePath import rootPath

class GetDir(object):
    """
    This is a class
    """
    def __init__(self):
        self.time = time.strftime("%Y-%m-%d")
        
    def getDirectory(self):
        """
        This is a main spider
        """
        backdir = rootPath + "data/primaryData/Car4s/"
        Datedir = backdir + self.time + "/"
        if not os.path.exists(Datedir):
            os.makedirs(Datedir)
            return Datedir
        else:
            return Datedir
            
    def outFile(self, outFile):
        """
        This is to get out file
        """
        if os.path.exists(outFile):
            os.system("rm " + outFile)
    
        
