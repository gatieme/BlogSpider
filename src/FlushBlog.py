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

from DealBlogThread import DealBlogThread
from FlushBlogThread import FlushBlogThread




#   刷新博客进程

class FlushBlog:
    """
        刷新博客进程

        包括以下成员:

        self.dealBlog   处理博客类

        self.maxThread  同时刷新博客的最大线程数目

        self.semphore   刷新博客线程的信号量

        self.flushMode  sequential顺序刷新, random随机访问

       # self.unflushList 不刷新列表， 在配置文件中添加，添加后的地址将永远不进行刷新
    """

    def __init__(self, pageUrl, pageSize, maxThread, flushMode = "random"):
        #  初始化成员
        self.dealBlogThread  = DealBlogThread(pageUrl, pageSize)            #  处理博客类
        self.flushBlogThread = FlushBlogThread(maxThread, flushMode)

        signal.signal(signal.SIGTERM, self.SignalHandler)
        signal.signal(signal.SIGINT, self.SignalHandler)                    #  永远不刷新的博客列表


    def SignalHandler(self, sig, frame):
        """
        信号处理函数

        python中得thread的一些机制和C/C++不同：
            在C/C++中，主线程结束后，其子线程会默认被主线程kill掉。
            而在python中，主线程结束后，会默认等待子线程结束后，主线程才退出。

        python对于thread的管理中有两个函数：join和setDaemon

            join：如在一个线程B中调用threada.join()，则threada结束后，线程B才会接着threada.join()往后运行。
            setDaemon：主线程A启动了子线程B，调用b.setDaemaon(True)，则主线程结束时，会把子线程B也杀死，与C/C++中得默认效果是一样的。
        """
        try :

            T.stop( )
            T.join()

        except Exception, ex:

            init(autoreset = True)
            print ""
            print (Fore.RED + Style.BRIGHT + u"用户输入Ctrl+C 程序终止...")

            exit(0)

    def KeyBoardHandle(self):
        """
        """
        while self.FlushStopped == False or self.DealStopped == False :
            input = raw_input()
            #print "键入", input

            if (input == "q" or input == "quit"):

                print "接收到用户的指令", input, "程序准备退出..."
                self.Stop( )

            elif(input == "ls" or input == "list"):

                print "列出所有的线程的信息..."
                for thread in self.threadPools:
                        print "线程", thread.name
                print "总刷新次数 %d, 博客文章数目 %d" % (self.totalFlushCount, len(self.dealBlog.blogs))



    def Run(self):
        """
        刷新博客
        """
        self.dealBlogThread.Start( )
        self.flushBlogThread.Start( )
        self.Key



if __name__ == "__main__":

    #flushBlog = FlushBlogThread(pageUrl, pageSize, maxThread, flushMode)

    #flushBlog.RunFunction( )

    pass
