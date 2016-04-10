#!/usr/bin/env python
# encoding: utf-8

import TerminalColor

from colorama import init, Fore, Back, Style

#import time, datetime
from datetime import *

# 博客类

class Blog:
    """
        本类是现实中博客的类

    """
    def __init__(self, url, title, postdate, postdays, view, comments):

        self.url         =     url          # 博客的地址

        self.title       =     title        # 博客的标题

        self.postdate    =     postdate    # 博客的发表时间

        self.postdays    =     postdays    # 已经发表的天数

        self.view        =     view        # 博客的阅读次数

        self.comment     =     comments    # 博客的评论条数


    def Show(self):

        #print "当前访问的博客地址", self.url

        #print TerminalColor.UseStyle(u"博客标题", fore = 'white'),
        #print TerminalColor.UseStyle(self.title.decode("utf-8"), fore = 'blue'),

        #print TerminalColor.UseStyle(u"博客地址", fore = 'white'),
        #print TerminalColor.UseStyle(self.url[-8:].decode("utf-8"), fore = 'blue'),

        #print TerminalColor.UseStyle(u"发表时间", fore = 'white'),
        #print TerminalColor.UseStyle(self.postdate.decode("utf-8"), fore = 'blue'),

        #print TerminalColor.UseStyle(u"阅读次数", fore = 'white'),
        #print TerminalColor.UseStyle(self.view, fore = 'red'),

        #print TerminalColor.UseStyle(u"评论条数", fore = 'white'),
        #print TerminalColor.UseStyle(self.comment, fore = 'red')

        init(autoreset = True)

        print (Fore.WHITE + u"博客标题"),
        print (Fore.BLUE + self.title.decode("utf-8")),

        print (Fore.WHITE + u"博客地址"),
        print (Fore.BLUE + self.url[-8:].decode("utf-8")),


        #print self.postdate.date( )
        print (Fore.WHITE + u"发表时间"),
        print (Fore.BLUE + self.postdate.strftime("%Y-%m-%d %X")),

        print (Fore.WHITE + u"发表天数"),
        print (Fore.BLUE + str(self.postdays))

        print (Fore.WHITE + u"阅读次数"),
        print (Fore.RED + str(self.view)),

        print (Fore.WHITE + u"评论条数"),
        print (Fore.RED + str(self.comment))
