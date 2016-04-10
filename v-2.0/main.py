#!/usr/bin/env python
#coding=utf-8

import sys

import argparse
import ConfigParser


from FlushBlogProcess import FlushBlogProcess
from FlushBlogThread import FlushBlogThread



if __name__ == "__main__" :

    #  重新设置编码集
    reload(sys)
    sys.setdefaultencoding( "utf-8" )

    sys.setrecursionlimit(1000000)

    if len(sys.argv) > 1:               #  如果在程序运行时，传递了命令行参数

        #  打印传递的命令行参数的信息
        print "您输入的所有参数共 %d 个，信息为 sys.argv = %s" % (len(sys.argv), sys.argv)

        for i, eachArg in enumerate(sys.argv):

            print "[%d] = %s" % (i, eachArg)


        #  创建一个解析对象
        #  然后向该对象中添加你要关注的命令行参数和选项
        #  每一个add_argument方法对应一个你要关注的参数或选项
        #  最后调用parse_args()方法进行解析
        #  解析成功之后即可使用

        parser      = argparse.ArgumentParser( )
        parser.add_argument("-u", "--pageurl", dest = "pageUrl_parser", help = "The url of your blog page...")
        parser.add_argument("-s", "--pagesize", dest = "pageSize_parser", help = "Your page size...", type = int)
        parser.add_argument("-t", "--maxthread", dest = "maxThread_parser", help = "Your max thread size...", type = int)
        parser.add_argument("-m", "--flushmode", dest = "flushMode_parser", help = "Your fulsh mode...")

        args        = parser.parse_args( )

        pageUrl     = args.pageUrl_parser
        pageSize    = args.pageSize_parser
        maxThread   = args.maxThread_parser
        flushMode   = args.flushMode_parser

    else:       #  否则如果没有传递命令行参数
        #  从配置文件中读取参数信息
        cf        = ConfigParser.ConfigParser( )
        cf.read("fb.conf")

        pageUrl   = cf.get("url_conf", "pageUrl")
        pageSize  = int(cf.get("url_conf", "pageSize"))

        maxThread = int(cf.get("flush_conf", "maxThread"))
        flushMode = cf.get("flush_conf", "flushMode")
    #    unflushList   = cf.get("flush_conf", "unflush").split(',')



    print u"获取到的命令行参数或者配置文件信息如下："
    print u"博客列表地址 pageUrl = ", pageUrl
    print u"博客列表篇数 pageSize =", pageSize
    print u"刷新线程数目 maxThread = ", maxThread
    print u"刷新博客方式 flushMode =", flushMode


    flushBlog = FlushBlogThread(pageUrl, pageSize, maxThread, flushMode)
    flushBlog.Run( )

    #flushBlog = FlushBlogProcess(pageUrl, pageSize, maxThread, flushMode)
    #flushBlog.Run( )

