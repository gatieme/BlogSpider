#/usr/bin/python
#-*- coding: utf-8 -*-



import urllib2

import sys

import time

import threading

import random

import signal

#import TerminalColor

from colorama import init, Fore, Style



from Blog import Blog

from DealBlog import DealBlog

from FlushBlogProcess import FlushBlogProcess


def  FlushBlogThreadPool :
    """
    """

    def __init__(self, pageUrl, pageSize, maxThread, flushMode = "random"):

        self.dealBlog  = DealBlog(pageUrl, pageSize)            #  处理博客类

        self.maxThread = maxThread                              #  同时刷新博客的最大线程数目

        self.semphore  = threading.BoundedSemaphore(maxThread)  #  刷新博客线程的信号量

        self.flushMode = flushMode     
        


    def RandomFlushBlog(self):
        """
        随机访问每一篇博客
        """
        index = random.randint(0, len(self.dealBlog.blogs) - 1)

        print "index = ", index

        blog = self.dealBlog.blogs[index]

        
    def SequentialFlushBlog(self):

"""
"""
if __name__ "__main__" :
