#!/usr/bin/env python
# encoding: utf-8

import sys

from FlushBlogProcess  import FlushBlogProcess


if __name__ == "__main__" :

    # 测试正则表达式

    reload(sys)

    sys.setdefaultencoding( "utf-8" )

    # TestGetBlogUrl()   #  测试匹配字符串

    # TestReChinese( )


    flushBlog = FlushBlogProcess("http://blog.csdn.net/gatieme/article/list/", 9, 5, "random")

    flushBlog.Run( )


