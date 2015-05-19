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

    def __init__(self, pageUrl, pageSize):

        self.pageSize   =     pageSize    # 博客页面数目

        self.pageUrl    =     pageUrl      # 博客源地址

        self.blogPages  =     []            # 博客页面的地址

        self.blogs      =     []

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





    # 从博客页面中获取到每个博客的地址

    def GetBlogUrl(self):

        print u"开始获取博客地址......"

        print u"依次访问每个博客列表页面"

        for url in self.blogPages:                # 访问每一个博客页面

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

                else:

                    pass  #其他异常的处理

            # print page



            # 从博客页面中匹配出每个博客的地址

            print u"开始用正则表达式匹配博客信息......"



            # 从博客页面中匹配出每个博客的地                                                                           址

            reHtml = r'<span class="link_title"><a href="(.*?)">\s*(.*?)\s*</a></span>.*?<span class="link_postdate">(.*?)</span>\s*<span class="link_view" title=".*?"><a href="(.*?)" title=".*?">.*?</a>(.*?)</span>\s*<span class="link_comments" title=".*?"><a href="(.*?)#comments" title=".*?" onclick=".*?">.*?</a>(.*?)</span>'

            pattern = re.compile(reHtml, re.S)

            myItems = re.findall(pattern, unicodePage)



            print u"从博客列表页面中匹配出 %d 条博客信息" % (len(myItems))    # print myItems

            for item in myItems:

                # print "#------------------------------------------------------"

                # print item[0].replace("\n", "")         # 博客地址URL1(标题附带)

                # print item[1].replace("\n", "")         # 博客标题

                # print item[2].replace("\n", "")         # 博客发表时间

                # print item[3].replace("\n", "")         # 博客地址URL2(阅读次数附带)

                # print item[4].replace("\n", "")         # 博客阅读次数信息

                # print item[5].replace("\n", "")         # 博客地址URL3(评论条数附带)

                # print item[6].replace("\n", "")         # 博客评论条数

                # print "#-----------------------------------------------------"

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

                    view = item[4].replace("\n","")
                    view = int(view[1:-1])

                    comments = item[6].replace("\n","")
                    comments = int(comments[1:-1])

                    blog = Blog(url, title, postdate, view, comments)

                    blog.Show( )

                    self.blogs.append(blog)    # 将从页面中匹配出来的博客信息添加如博客列表中

                else :

                    print u"匹配出现问题..."

                    print "URL1 = ", url1

                    print "URL2 = ", url2

        return self.blogs
