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



#   刷新博客进程

class FlushBlogThread:
    """
        刷新博客进程

        包括以下成员:

        self.dealBlog   处理博客类

        self.maxThread  同时刷新博客的最大线程数目

        self.semphore   刷新博客线程的信号量

        self.flushMode  sequential顺序刷新, random随机访问

       # self.unflushList 不刷新列表， 在配置文件中添加，添加后的地址将永远不进行刷新
    """

    def __init__(self, maxThread, flushMode = "random"):

        #---------------------
        #  初始化成员
        #---------------------
        self.maxThread = maxThread                              #  同时刷新博客的最大线程数目

        self.FlushStopped = False                               #  FlushBlogThread线程的运行标识

        self.semphore  = threading.BoundedSemaphore(maxThread)  #  刷新博客线程的信号量
        self.flushMode = flushMode                              #  sequential顺序刷新, random随机访问

        self.threadPools = []   # 线程池

        self.totalFlushCount = 0

        #  依据刷新方式设置线程的函数
        if self.flushMode == "random":

            self.threadFunction = self.RandomFlushBlogFunction

        elif self.flushMode == "sequential":

            self.threadFunction = self.SequentialFlushBlogFunction


    def AccessBlog(self, blog):
        """

        函数功能： 访问blog的一次, 并将博客访问次数加1

        参数     ：

            blog 待刷新的博客信息
        """

        req = urllib2.Request(blog.url)

        req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")

        try:

            cn = urllib2.urlopen(req)

            #print TerminalColor.UseStyle("Now, check the url = "), TerminalColor.UseStyle(blog.url[-8:], fore = 'green')

            #init(autoreset = True)
            #print("Now, check the url = "),
            #print(Fore.GREEN + blog.url[-8:] + ", " +blog.title)
            #print("")

            blog.flushcount += 1        #  刷新次数增加1
            self.totalFlushCount += 1   #  总刷新次数增加1
            #blog.Show( )
            cn.close( )

        except urllib2.URLError, e:

            if hasattr(e, "reason"):

                print "Failed to reach the server"
                print "The reason:", e.reason

            elif hasattr(e, "code"):

                print "The server couldn't fulfill the request"
                print "Error code:", e.code
                print "Return content:", e.read( )

            else:

                pass  #其他异常的处理

#

#        self.semphore.release( )


    def ShowBlog(self, blog, index, length):
        # show blog information
        init(autoreset = True)
        #print(Fore.RED + "[" + str(index) + "/" + str(len(self.dealBlog.blogs)) + "]"),
        print(Fore.RED + "[" + str(index).zfill(3) + "/" + str(length).zfill(3) + "]"),
        print("Now " + Fore.WHITE + "(" + str(blog.flushcount).zfill(4) + ")"),
        print("url = " + Fore.BLUE + blog.url[-8:]),
        print("title = " + Fore.GREEN + blog.title)
        print("")


    def RandomFlushBlogFunction(self):
        """
        随机访问每一篇博客
        """
        while self.FlushStopped == False:

            if (len(self.dealBlog.blogs) == 0):
                print "没有博客待刷新..."
                time.sleep(5)
                continue

            #  随机生成一个索引index
            index = random.randint(0, len(self.dealBlog.blogs) - 1)

            #  取出当前的索引index的博客信息
            blog = self.dealBlog.blogs[index]
            if (self.FlushStopped == True):
                break

            self.semphore.acquire( )
            self.AccessBlog(blog)
            self.ShowBlog(blog, index, len(self.dealBlog.blogs))
            self.semphore.release( )
            time.sleep(random.randint(8, 18))
            #print "线程退出..."



    def SequentialFlushBlogFunction(self):
        """
        顺序访问每一篇博客
        """

        index = 0
        while self.FlushStopped == False:
            if (len(self.dealBlog.blogs) == 0):
                print "没有博客待刷新..."
                time.sleep(5)
                continue
            #for blog in self.dealBlog.blogs:
            index = (index + 1) % len(self.dealBlog.blogs)
            blog = self.dealBlog.blogs[index]
            if (self.FlushStopped == True):
                break

            self.semphore.acquire( )
            self.AccessBlog(blog)
            self.ShowBlog(blog, index, len(self.dealBlog.blogs))
            self.semphore.release( )
            time.sleep(random.randint(8, 18))
        #print "线程退出..."



    def Stop(self):
        self.FlushStopped = True
        print "等待所有线程安全退出..."

        for thread in self.threadPools:
            print "线程", thread.name, "终止..."
            thread.join( )
        print "所有的线程都已经终止, 程序退出..."
        exit(0)



    def Start(self) :
        """
        刷新博客
        """
        # 先创建线程对象
        for thread in xrange(0, self.maxThread):
            self.threadPools.append(threading.Thread(name = "FlushBlog-" + str(thread + 1), target = self.threadFunction))


        # 启动所有线程
        for thread in self.threadPools :
            print "线程", thread.name, "启动..."
            thread.start( )
