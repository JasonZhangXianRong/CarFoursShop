"""
get root path
"""
import sys
import os
__all__ = ['rootPath']
Path = os.path.split(os.path.realpath(__file__))[0]
ProPath = Path[:Path.find("crawl-brand")]
rootPath = ProPath + "crawl-brand/"
