#!/usr/bin/env python
# encoding: utf-8

import urllib2

import re

#import TerminalColor

from Blog import Blog


from colorama import init, Fore, Back, Style

import time, datetime

# 刷新博客类

class DealBlog:

    # 刷新博客类的初始化

    def __init__(self, pageUrl = "", pageSize = 0):

        self.pageSize   =     pageSize      #  博客页面数目

        self.pageUrl    =     pageUrl       #  博客源地址

        self.blogPages  =     []            #  博客页面的地址

        self.blogs      =     []            #  待刷新的博客地址列表

        #   目前设置为博客发表日期在一个月内的博客不进行刷新
        self.noneBlogs  =     []            #  不期望刷新的地址列表

        self.sysTime    =     time.localtime( )
        self.sysTime    =     datetime.datetime(*self.sysTime[:6])

        print u"博客页面: ", self.pageUrl

        print u"博客页数 = ", self.pageUrl





    # 从博客页面中获取到所有页面的地址

    def GetBlogPage(self):

        for pos in range(1, self.pageSize + 1):

            currPageUrl = self.pageUrl + str(pos)

            #print u"当前博客页面地址: ", TerminalColor.UseStyle(currPageUrl, fore = "blue")

            init(autoreset = True)

            print u"当前博客页面地址: ",
            print (Fore.BLUE + currPageUrl)
            #print(Fore.RESET + Back.RESET + Style.RESET_ALL)

            self.blogPages.append(currPageUrl) # 每个博客页面的地址



        print u"获取到的博客页面信息[SUCCESS]:"

        print self.blogPages



    def GetAccessUrlHtml(self, url):
        # 建立去请求访问每个页面
        req = urllib2.Request(url)                # 建立页面请求
        req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)")

        print u"获取到博客列表页面HTML源码"

        try:
            cn = urllib2.urlopen(req)
            print u"开始访问博客列表页面: ", url

            page = cn.read( )

            unicodePage = page.decode("utf-8")

            cn.close( )


        except urllib2.URLError, e:

            if hasattr(e, "reason"):

                print "Failed to reach the server"
                print "The reason:", e.reason

            elif hasattr(e, "code"):

                print "The server couldn't fulfill the request"
                print "Error code:", e.code
                print "Return content:", e.read()
                print "Return content:", e.read()
            else:
                pass  #其他异常的处理

        return unicodePage

    def GetBlogFromPageHtml(self, unicodePage):
        """
        """
        # 从博客页面中匹配出每个博客的地址

        print u"开始用正则表达式匹配博客信息......"

        # 从博客页面中匹配出每个博客的地                                                                           址

        # 匹配出所有的博客信息(不匹配带置顶标识的博客信息)
        #reHtml = r'<span class="link_title"><a href="(.*?)">\s*(.*?)\s*</a>\s*</span>.*?<span class="link_postdate">(.*?)</span>\s*<span class="link_view" title=".*?"><a href="(.*?)" title=".*?">.*?</a>(.*?)</span>\s*<span class="link_comments" title=".*?"><a href="(.*?)#comments" title=".*?" onclick=".*?">.*?</a>(.*?)</span>'
        # 匹配出带置顶标识的博客信息
        #reHtml = r'<span class="link_title"><a href="(.*?)">(\s*<font color="red">.*?</font>|\s*)\s*(.*?)\s*</a>\s*</span>.*?<span class="link_postdate">(.*?)</span>\s*<span class="link_view" title=".*?"><a href="(.*?)" title=".*?">.*?</a>(.*?)</span>\s*<span class="link_comments" title=".*?"><a href="(.*?)#comments" title=".*?" onclick=".*?">.*?</a>(.*?)</span>'
        #reHtml = r'<span class="link_title"><a href="(.*?)">(\s*<font color="red">\[置顶\]</font>(.*?)\s*|\s*(.*?)\s*)</a>\s*</span>.*?<span class="link_postdate">(.*?)</span>\s*<span class="link_view" title=".*?"><a href="(.*?)" title=".*?">.*?</a>(.*?)</span>\s*<span class="link_comments" title=".*?"><a href="(.*?)#comments" title=".*?" onclick=".*?">.*?</a>(.*?)</span>'
        reHtml = r'<span class="link_title"><a href="(.*?)">(?:\s*<font color="red">.*?</font>|\s*)\s*(.*?)\s*</a>\s*</span>.*?<span class="link_postdate">(.*?)</span>\s*<span class="link_view" title=".*?"><a href="(.*?)" title=".*?">.*?</a>(.*?)</span>\s*<span class="link_comments" title=".*?"><a href="(.*?)#comments" title=".*?" onclick=".*?">.*?</a>(.*?)</span>'


        pattern = re.compile(reHtml, re.S)

        myItems = re.findall(pattern, unicodePage)

        print u"从博客列表页面中匹配出 %d 条博客信息" % (len(myItems))    # print myItems

        for item in myItems:
            #print item[1]
            if 0:           #   for debug
                 print "#------------------------------------------------------"
                 print item[0].replace("\n", "")         # 博客地址URL1(标题附带)
                 print item[1].replace("\n", "")         # 博客标题
                 print item[2].replace("\n", "")         # 博客发表时间
                 print item[3].replace("\n", "")         # 博客地址URL2(阅读次数附带)
                 print item[4].replace("\n", "")         # 博客阅读次数信息
                 print item[5].replace("\n", "")         # 博客地址URL3(评论条数附带)
                 print item[6].replace("\n", "")         # 博客评论条数
                 print "#-----------------------------------------------------"

            urlTitle = item[0].replace("\n", "")
            urlView = item[3].replace("\n", "")
            urlComments = item[5].replace("\n", "")
            # 由于匹配时使用了贪婪模式, 为了匹配出现错误，
            # 将某一篇的标题与另一篇博客的发表时间, 阅读次数或者评论条数混淆的匹配成一篇博客信息
            # 因此在匹配时，重复的匹配了博客的地址信息
            # 当且仅当，博客标题附带的地址信息与博客阅读次数以及评论条数附带的地址信息时同一篇博客的地址时，
            # 我们才认为匹配成功

            if (urlTitle == urlView) and (urlTitle == urlComments):

                url = "http://blog.csdn.net" + item[0].replace("\n","")
                title = item[1].replace("\n", "")

                postdate = item[2].replace("\n", "").decode("utf-8")
                postdate = time.strptime(item[2].replace("\n", ""), "%Y-%m-%d %H:%M")
                postdate = datetime.datetime(*postdate[:6])
                #print "POSTDATE = ", postdate
                postdays = (self.sysTime - postdate).days   #  已经发表的天数
                if (postdays < 0):
                    print "当前系统时间小于博客发布时间, 可能系统的时间不正确, 请注意检查..."
                    postdays = 1

                view = item[4].replace("\n","")
                view = int(view[1:-1])

                comments = item[6].replace("\n","")
                comments = int(comments[1:-1])

                blog = Blog(url, title, postdate, postdays, view, comments)
                blog.Show( )

                # 将从页面中匹配出来的博客信息添加如博客列表中
                if blog.postdays  > 0:

                    self.blogs.append(blog)
                    print u"本博客已经发表了 %d 天，超过一个月, 添加到待刷新列表..."  % (blog.postdays)

                else:

                    self.noneBlogs.append(blog)
                    print u"本博客刚刚发表了 %d 天，不足一个月, 添加到拒绝刷新列表..." % (blog.postdays)

            else :

                print u"匹配出现问题..."

        return self.blogs




    # 从博客页面中获取到每个博客的地址
    def GetBlogUrl(self):

        print u"开始获取博客地址......"
        print u"依次访问每个博客列表页面"

        for url in self.blogPages:                # 访问每一个博客页面

            print u"开始读取博客列表", url
            unicodePage = self.GetAccessUrlHtml(url)

            print u"开始从博客列表中匹配博客的信息"
            blogs = self.GetBlogFromPageHtml(unicodePage)



    def GetBlogPageFunction(self):
        """
        """
        #---------------------
        #  获取到博客页面的信息
        #---------------------
        self.dealBlog.GetBlogPage( )            # 检索出所有的博客列表页面

        self.dealBlog.GetBlogUrl( )             # 获取到每个博客的页面信息

        self.dealBlog.ListBlogs( )



    def ListBlogs(self):
        """
        """
        print "--------------------------------------------------"
        print u"共计发现博客 %d 篇" % (len(self.dealBlog.blogs) + len(self.dealBlog.noneBlogs))
        print u"待刷新博客 %d 篇，刷新方式 %s" % (len(self.dealBlog.blogs),  self.flushMode)
        print u"拒绝刷新博客 %d 篇" %(len(self.dealBlog.noneBlogs))
#       print u"永不刷新博客 %d 篇" %(len(self.dealBlog.unflushList))
        print "--------------------------------------------------"






if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    currtime = time.localtime( )
    print datetime.datetime(*currtime[:6])
    db = DealBlog( )
    unicodePage = db.GetAccessUrlHtml("http://blog.csdn.net/gatieme/article/list/1")
    blogs = db.GetBlogFromPageHtml(unicodePage)
    for blog in blogs:
        print blog.title
