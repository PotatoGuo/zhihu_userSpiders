# zhihu_userSpiders
知乎用户分布式爬虫

zhihu_spider：利用scrapy_redis，实现分布式。

zhihu_spider2:基本以scrapy_redis为基础，简化了其中一些代码，关键是重写了dupefilter中request_seen方法，利用bloomfilter过滤request，节省空间。

其中start_urls需要提前存入redis，并且zhihu_spider2中，start_urls必须存入redis的set中，key为'start_urls'。

爬的是移动端知乎页面，useragent必须是移动端的。

zhihu_spider2经过测试，用一台机子，网络是校园网，一个上午（3小时），只爬followees(因为知乎大V的followers太多，会发送很多ajax请求)，爬了近6000个用户资料。

运行环境：

系统：ubuntu14.04

db：mongodb和redis

python：2.7.6

bloomfilter源码（BloomFilter.py）是直接来自大神的blog：https://pycntech.github.io/%E5%9F%BA%E4%BA%8ERedis%E7%9A%84Bloomfilter%E5%8E%BB%E9%87%8D%EF%BC%88%E9%99%84Python%E4%BB%A3%E7%A0%81%EF%BC%89-%E4%B9%9D%E8%8C%B6.html

bloomfilter的原理：http://blog.csdn.net/guoziqing506/article/details/52852515
                  http://blog.csdn.net/hguisu/article/details/7866173
