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

        #---------------------
        #  增加终止信号的处理
        #---------------------
        signal.signal(signal.SIGTERM, self.SignalHandler)
        signal.signal(signal.SIGINT, self.SignalHandler)                    #  永远不刷新的博客列表

        #---------------------
        #  初始化成员
        #---------------------
        self.dealBlog  = DealBlog(pageUrl, pageSize)            #  处理博客类

        self.maxThread = maxThread                              #  同时刷新博客的最大线程数目


        self.semphore  = threading.BoundedSemaphore(maxThread)  #  刷新博客线程的信号量

        self.flushMode = flushMode                              #  sequential顺序刷新, random随机访问

        self.totalFlushCount = 0

        #  依据刷新方式设置线程的函数
        if self.flushMode == "random":

            self.threadFunction = self.RandomFlushBlogFunction

        elif self.flushMode == "sequential":

            self.threadFunction = self.SequentialFlushBlogFunction


        self.threadPools = []   # 线程池
        self.DealStopped = False                                #  DealBlog线程的运行标识
        self.FlushStopped = False                               #  FlushBlogThread线程的运行标识

        self.threadDeal = threading.Thread(name = "DealBlog", target = self.DealBlogFunction)
        #self.threadPools.append(self.threadDeal)
        #self.GetBlogPageFunction( )
        for thread in xrange(0, self.maxThread):
            self.threadPools.append(threading.Thread(name = "FlushBlog-" + str(thread + 1), target = self.threadFunction))



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



    def SignalHandler(self, sig, frame):
        """
        信号处理函数

        python中得thread的一些机制和C/C++不同：
            在C/C++中，主线程结束后，其子线程会默认被主线程kill掉。
            而在python中，主线程结束后，会默认等待子线程结束后，主线程才退出。

        python对于thread的管理中有两个函数：join和setDaemon

            join：如在一个线程B中调用thread.join()，则threada结束后，线程B才会接着threada.join()往后运行。
            setDaemon：主线程A启动了子线程B，调用b.setDaemaon(True)，则主线程结束时，会把子线程B也杀死，与C/C++中得默认效果是一样的。
        """
        print "接收到用户的终止信号..."
        try :

            self.Stop( )

        except Exception, ex:

            init(autoreset = True)
            print ""
            print (Fore.RED + Style.BRIGHT + u"用户输入Ctrl+C 程序终止...")

            exit(0)


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
                if self.DealStopped == False :
                    print "线程", self.threadDeal.name
                    print "当前检索出的博客数目 %d" % (len(self.dealBlog.blogs))
                for thread in self.threadPools:
                        print "线程", thread.name
                print "总刷新次数 %d, 博客文章数目 %d" % (self.totalFlushCount, len(self.dealBlog.blogs))


    def IsStopped(self) :
        return self.FlushStopped == True

    def IsRunning(self) :
        return self.FlushStopped == False



    def DealBlogFunction(self):
        """
        """
        #---------------------
        #  获取到博客页面的信息
        #---------------------
        self.dealBlog.GetBlogPage( )            # 检索出所有的博客列表页面
        self.dealBlog.GetBlogUrl( )             # 获取到每个博客的页面信息
        print "DealBlog线程完成了自己的工作, 正在准备退出..."
        self.ListBlogs( )
        self.DealStopped = True

    def ListBlogs(self):
        """
        """
        print "--------------------------------------------------"
        print u"共计发现博客 %d 篇" % (len(self.dealBlog.blogs) + len(self.dealBlog.noneBlogs))
        print u"待刷新博客 %d 篇，刷新方式 %s" % (len(self.dealBlog.blogs),  self.flushMode)
        print u"拒绝刷新博客 %d 篇" %(len(self.dealBlog.noneBlogs))
#       print u"永不刷新博客 %d 篇" %(len(self.dealBlog.unflushList))
        print "--------------------------------------------------"


    def Flush(self):

        self.GetBlogPageFunction( )
        self.treadFunction( )

    def Run(self) :
        """
        刷新博客
        """
        #mutex = threading.Lock()

        print "线程", self.threadDeal.name, "启动..."
        self.threadDeal.start( )

        # 启动所有线程
        for thread in self.threadPools :
            print "线程", thread.name, "启动..."
            thread.start( )

        print "主线程开始接收用户指令..."
        #self.threadPools.append(threading.Thread(target = self.KeyBoardHandle))
        self.KeyBoardHandle( )
