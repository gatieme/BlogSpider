#!/usr/bin/env python
#coding=utf-8

import sys

from FlushBlogProcess  import FlushBlogProcess




if __name__ == "__main__" :

    # 测试正则表达式

    reload(sys)
    sys.setdefaultencoding( "utf-8" )

    flushBlog = FlushBlogProcess("http://blog.csdn.net/gatieme/article/list/", 9, 5, "random")

    flushBlog.Run( )


