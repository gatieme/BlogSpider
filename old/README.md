# FlushBlogs


#version
0.0.1
    版本更新自0.0.1，引入 [顺序/随机刷新机制]

    添加了顺序访问/刷新sequential和随机访问/刷新random两种不同的刷新方式
    更新了模块结构, 使程序结构更加清晰


0.0.2
    版本更新自0.0.2，引入 [拒绝刷新列表]

    发表时间不足一个月的不加入刷新列表，而是进入拒绝刷新列表.
    是博客的刷新机制更加人性化，更加真实

    [2015-05-22 13:31:40]
    在博客信息中添加了已经发表日期postdays，优化了发表日期不足一个月不足拒绝刷新机制


0.0.3
    版本更新自0.0.3，引入 [命令行参数] 和 [配置文件]

    命令行参数使用argparser模块实现
    -u  --pageurl   指定待刷新的博客列表页面的地址
    -s  --pageSize  指定带刷新博客列表页面的篇数
    -t  --maxThread 用于指定刷新博客时的线程数
    -m  --flushMode 用于指定刷新博客的模式[顺序访问/刷新和随机访问/刷新]
    ./main.py -u http://blog.csdn.net/gatieme/article/list/ -s 9 -t 5 -m random

    配置文件信息
    [url_conf]
    pageUrl   =  http://blog.csdn.net/gatieme/article/list/
    pageSize  =  9


    [flush_conf]
    maxThread =  5
    flushMode =  random
