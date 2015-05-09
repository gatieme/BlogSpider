#!/usr/bin/env python
# encoding: utf-8

import TerminalColor



# 博客类

class Blog:
    """
        本类是现实中博客的类

    """
    def __init__(self, url, title, postdate, view, comments):

        self.url         =     url          # 博客的地址

        self.title       =     title        # 博客的标题

        self.postdate    =     postdate    # 博客的发表时间

        self.view        =     view        # 博客的阅读次数

        self.comment     =     comments    # 博客的评论条数



    def Show(self):

        #print "当前访问的博客地址", self.url

        print TerminalColor.UseStyle("博客标题", fore = 'white'),
        print TerminalColor.UseStyle(self.title, fore = 'blue'),

        print TerminalColor.UseStyle("博客地址", fore = 'white'),
        print TerminalColor.UseStyle(self.url[-8:], fore = 'blue'),

        print TerminalColor.UseStyle("发表时间", fore = 'white'),
        print TerminalColor.UseStyle(self.postdate, fore = 'blue'),

        print TerminalColor.UseStyle("阅读次数", fore = 'white'),
        print TerminalColor.UseStyle(self.view, fore = 'red'),

        print TerminalColor.UseStyle("评论条数", fore = 'white'),
        print TerminalColor.UseStyle(self.comment, fore = 'red')

