#/usr/bin/python
#-*- coding: utf-8 -*-


import urllib2


import sys

import time

import threading

import random

import TerminalColor

from Blog import Blog

from DealBlog import DealBlog




#   刷新博客进程

class FlushBlogProcess:
    """
        刷新博客进程

        包括以下成员:

        self.dealBlog   处理博客类

        self.maxThread  同时刷新博客的最大线程数目

        self.semphore   刷新博客线程的信号量

        self.flushMode  sequential顺序刷新, random随机访问
    """

    def __init__(self, pageUrl, pageSize, maxThread, flushMode = "random"):

        self.dealBlog  = DealBlog(pageUrl, pageSize)            #  处理博客类

        self.maxThread = maxThread                              #  同时刷新博客的最大线程数目

        self.semphore  = threading.BoundedSemaphore(maxThread)  #  刷新博客线程的信号量

        self.flushMode = flushMode                              # sequential顺序刷新, random随机访问


    def AccessBlog(self, blog):

        """

        函数功能： 访问blog的一次, 并将博客访问次数加1

        参数     ：

            blog 待刷新的博客信息
:wq
        """

        req = urllib2.Request(blog.url)

        req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")



        try:

            cn = urllib2.urlopen(req)

            print TerminalColor.UseStyle("Now, check the url = "), TerminalColor.UseStyle(blog.url[-8:], fore = 'green')

            blog.view = blog.view + 1

            blog.Show( )

            cn.close( )

        except urllib2.URLError, e:

            if hasattr(e, "reason"):

                print "Failed to reach the server"

                print "The reason:", e.reason

            elif hasattr(e, "code"):

                print "The server couldn't fulfill the request"

                print "Error code:", e.code

                print "Return content:", e.read()

            else:

                pass  #其他异常的处理

        time.sleep(2)

        self.semphore.release( )



    def RandomFlushBlog(self):
        """
        随机访问每一篇博客
        """
        index = random.randint(0, len(self.dealBlog.blogs) - 1)

        #print "index = ", index

        blog = self.dealBlog.blogs[index]


        self.semphore.acquire( )

        T = threading.Thread(target = self.AccessBlog, args = (blog,))

        T.start( )

    def SequentialFlushBlog(self):
        """
        顺序访问每一篇博客
        """
        for blog in self.dealBlog.blogs:

            self.semphore.acquire( )

            T = threading.Thread(target = self.AccessBlog, args = (blog,))

            T.start( )


    def Run(self):

        """

        刷新博客

        """

        self.dealBlog.GetBlogPage( )            # 检索出所有的博客列表页面

        self.dealBlog.GetBlogUrl( )             # 获取到每个博客的页面信息


        print "--------------------------------------------------"

        print "共计发现博客 %d 篇, 刷新方式%s" % (len(self.dealBlog.blogs), self.flushMode)

        print "--------------------------------------------------"

        while 1 :
            if self.flushMode == "random":

                self.RandomFlushBlog( )

            elif self.flushMode == "sequential":

                self.SequentialFlushBlog( )




