#### 几个重要的配置文件说明
- scrapy.cfg: 项目配置文件。 
- settings.py: 该文件定义了一些设置，如用户代理，爬取延时等(详见: https://doc.scrapy.org/en/latest/topics/settings.html)。 
- items.py: 该文件定义了待抓取域的模型(详见: http://scrapy-chs.readthedocs.io/zh_CN/latest/intro/tutorial.html#item)。 
- pipelines.py: 该文件定义了数据的存储方式(处理要抓取的域)，可以是文件，数据库或者其他(详见: http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/item-pipeline.html)。 
- middlewares.py: 爬虫中间件，该文件可定义随机切换ip或者用户代理的函数(详见: http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/spider-middleware.html)。 
- spiders: 该目录下存储实际的爬虫代码(详见: http://scrapy-chs.readthedocs.io/zh_CN/latest/topics/spiders.html)。
---
#### scrapy startproject -h 几个重要的参数
```angular2
1、--logfile=FILE: 用来指定日志文件名及其存放位置，用法如下:
scrapy startproject --logfile="日志文件的路径地址" FirstProject

2、--loglevel=LEVEL, -L LEVEL: 控制日志信息的等级，默认为 DEBUG 模式，即会将对应的调试信息都输出。用法及日志的常见等级如下:
scrapy startproject --loglevel=ERROR FirstProject
或 scrapy startproject -L ERROR FirstProject

Scrapy 提供 5 层 logging 级别:

等级名	        含义
CRITICAL	严重错误(critical)
ERROR	一般错误(regular errors)
WARNING	警告信息(warning messages)
INFO	一般信息(informational messages)
DEBUG	调试信息(debugging messages)，常用于开发阶段

```