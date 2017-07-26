#! /usr/bin/env python2.7
#coding=utf-8

""" 
Read data from excel file and txt file.
Chinese word segmentation, postagger, sentence cutting and stopwords filtering function.

"""

import jieba
import jieba.posseg
jieba.initialize()
import xlrd
from pyExcelerator import *
import sys
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import os
import site
# sys.path.append("../")
import jieba.posseg as pseg
projectPath = os.path.abspath(os.path.dirname(sys.argv[0]))
#这个获取site-packages会有问题，在anaconda下会有问题，因为site-packages有可能不是sys.path数组中的最后一个
#python27PackagePath = os.path.abspath(sys.path[-1])
'''
    换成这种写法
    linux下：site-packages是数组中的第一个元素
    Windows下：site-packages是数组中的最后一个元素
'''
# python27PackagePath = site.getsitepackages()
import platform
sysstr = platform.system()
python27PackagePath = ''
if(sysstr =="Windows"):
    python27PackagePath = os.path.abspath(site.getsitepackages()[-1])
elif(sysstr == "Linux"):
    python27PackagePath = os.path.abspath(site.getsitepackages()[0])
else:
    print ("Other System tasks")
jiebaPath = python27PackagePath + "/jieba"

#Load user dictionary to increse segmentation accuracy
jieba.load_userdict(jiebaPath + "/userdict.txt")

stopWords = [line.strip().decode('utf-8') for line in open(jiebaPath + "/stopword.txt").readlines()]
# for word in stopWords:
#     print word



#################################################################################################
'''配置log'''
import log
# import logging
# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='nlp.log',
#                 filemode='a')
# #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)
# #################################################################################################


"""
input: An excel file with product review
	手机很好，很喜欢。
    三防出色，操作系统垃圾！
    Defy用过3年感受。。。
    刚买很兴奋。当时还流行，机还很贵
    ……
output:
    parameter_1: Every cell is a value of the data list. (unicode)
    parameter_2: Excel row number. (int)
"""
def get_excel_data(filepath, sheetnum, colnum, para):
    table = xlrd.open_workbook(filepath)
    sheet = table.sheets()[sheetnum-1]
    data = sheet.col_values(colnum-1)
    rownum = sheet.nrows
    if para == 'data':
        return data
    elif para == 'rownum':
        return rownum

'''
    读取指定的excel
    从开始行号获取指定的列
'''
def get_excel_data_by_multi_col(filepath,sheetnum,startRowNum,*columns):
    table = xlrd.open_workbook(filepath)
    sheet = table.sheets()[sheetnum - 1]
    rowCount = sheet.nrows
    colCount = sheet.ncols
    tempRow = []
    res = []
    for i in range(startRowNum-1,rowCount-1):
        row = sheet.row_values(i)
        for col in columns:
            if col <= colCount:
                tempRow.append(row[col-1])
        res.append(tempRow)
        tempRow = []
    return res



"""
input:
    parameter_1: A txt file with many lines
    parameter_2: A txt file with only one line of data
output:
    parameter_1: Every line is a value of the txt_data list. (unicode)
    parameter_2: Txt data is a string. (str)
"""

def get_txt_data(filepath, para):
    if para == 'lines':
        txt_file1 = open(filepath, 'r')
        txt_tmp1 = txt_file1.readlines()
        txt_tmp2 = ''.join(txt_tmp1)
        txt_data1 = txt_tmp2.decode('utf8').split('\n')
        txt_file1.close()
        return txt_data1
    elif para == 'line':
        txt_file2 = open(filepath, 'r')
        txt_tmp = txt_file2.readline()
        txt_data2 = txt_tmp.decode('utf8')
        txt_file2.close()
        return txt_data2




'''
    读取指定路径的数据文件 数据格式：评论id \t 文本 \t 话题id \t 时间
    :parameter1 数据文件路径
    :parameter return二维数组
'''
def get_input_data_by_path(inputPath):
    try:
        inputFile = open(inputPath,"r")
        liens = inputFile.readlines()
        res = []
        for line in liens:
            temp = line.decode("utf8").split("   ")
            res.append(temp)
        inputFile.close()
        return res
    except IOError as err:  # 使用as将异常对象，并将其赋值给一个标识符
        print('File Error:' + str(err))  # ‘+’用于字符串直接的连接
    finally:
        if 'inputFile' in locals():
            inputFile.close()

'''
    读取指定路径的数据文件(百度爬取) 数据格式：json
    :parameter1 数据文件路径
    :parameter return:[(topic_title,topic_time,topic_content),[(comment_content,comment_time,comment_praise_count),...]]
'''
import json
def get_input_data_from_qq(inputPath):
    try:
        inputFile = open(inputPath, "r")
        liens = inputFile.readlines()
        res = []
        for line in liens:
            jsonData = json.loads(line.decode("utf8"))
            # 获取话题标题
            title = jsonData['title']
            # 话题发布时间
            ttime = jsonData['time']
            # 话题内容
            t_content = jsonData['content']
            # 构造一个tuple存储话题
            topic = (title,ttime,t_content)
            # 遍历评论数据
            tempList = []
            for temp in jsonData['comment']:
                # 评论时间戳
                ctime = temp['time']
                # 评论内容
                c_content = temp['content']
                # 点赞数
                praise_count = temp['up']
                tempList.append((c_content,ctime,praise_count))
            res.append((topic,tempList))
        inputFile.close()
        return res
    except IOError as err:  # 使用as将异常对象，并将其赋值给一个标识符
        log.logger.error('File Error:' + str(err))  # ‘+’用于字符串直接的连接
    except Exception as e:
        log.logger.error('process json data error:' + str(e))
    finally:
        if 'inputFile' in locals():
            inputFile.close()



'''
    处理redis中的json数据
    return (任务ID,查询关键词，开始时间，结束时间，[((话题标题，话题发布时间，话题内容),[评论内容，评论发布时间，点赞数])...])
'''
def process_json_data_from_tencnetNews(content):
    try:
        res = []
        jsonData = json.loads(content.decode("utf8"))
        keyWord = jsonData['word']
        timeStart = jsonData['time_start']
        timeEnd = jsonData['time_end']
        userId = jsonData['userId'] #用户id
        jobId = jsonData['jobId']# 方案ID
        source = jsonData['source'] #来源
        #遍历话题列表
        for article in jsonData['articles']:
            # 获取话题标题
            title = article['title']
            # 话题发布时间
            ttime = article['time']
            # 话题内容
            t_content = article['content']
            # 原文链接
            t_url = article['url']
            # 构造一个tuple存储话题
            topic = (title,ttime,t_content,t_url)
            # 遍历评论数据
            tempList = []
            for temp in article['comment']:
                # 评论时间戳
                ctime = temp['time']
                # 评论内容
                c_content = temp['content']
                # 点赞数
                praise_count = temp['up']
                # 昵称
                nick = temp['nick']
                # 头像
                avatar = temp['head']
                tempList.append((c_content,ctime,praise_count,nick,avatar))
            res.append((topic,tempList))
        return (keyWord,timeStart,timeEnd,jobId,userId,source,res)
    except Exception as e:  # 使用as将异常对象，并将其赋值给一个标识符
        log.logger.error('process json data of qq error : ' + str(e))


'''
    处理redis中的评论数据
    return (任务ID,话题ID,来源,[评论内容，评论发布时间，点赞数,昵称,头像])
'''
def process_json_data_from_comment(content):
    try:
        jsonData = json.loads(content.decode("utf8"))
        jobId = jsonData['jobId']  # 方案ID
        source = jsonData['source']  # 来源
        topicId = jsonData['topicId']  # 话题ID
        # 遍历话题列表
        tempList = []
        for comment in jsonData['comments']:
            # 评论时间戳
            ctime = comment['time']
            # 评论内容
            c_content = comment['content']
            # 点赞数
            praise_count = comment['up']
            # 昵称
            nick = comment['nick']
            # 头像
            avatar = comment['head']
            tempList.append((c_content,ctime,praise_count,nick,avatar))
        return (jobId, topicId,source, tempList)
    except Exception as e:  # 使用as将异常对象，并将其赋值给一个标识符
        log.logger.error('process json data of qq error : ' + str(e))



"""
    结巴分词(过滤停用词)
    
input: 这款手机大小合适。
output:
    parameter_1: 这 款 手机 大小 合适 。(unicode)
    parameter_2: [u'\u8fd9', u'\u6b3e', u'\u624b\u673a', u'\u5927\u5c0f', u'\u5408\u9002', u'\uff0c']
"""

def segmentation(sentence, para):
    # 返回一个字符串
    seg_list = jieba.cut(sentence)
    if para == 'str':
        seg_result = ' '.join([word for word in seg_list if word not in stopWords and word != ' '])
        return seg_result
    # 返回一个list
    elif para == 'list':
        seg_result2 = [word for word in seg_list if word not in stopWords and word != ' ']
        return seg_result2


"""
input: '这款手机大小合适。'
output:
    parameter_1: 这 r 款 m 手机 n 大小 b 合适 a 。 x
    parameter_2: [(u'\u8fd9', ['r']), (u'\u6b3e', ['m']),
    (u'\u624b\u673a', ['n']), (u'\u5927\u5c0f', ['b']),
    (u'\u5408\u9002', ['a']), (u'\u3002', ['x'])]
    词性标注
"""

def postagger(sentence, para):
    if para == 'list':
        pos_data1 = jieba.posseg.cut(sentence)
        pos_list = []
        for w in pos_data1:
             pos_list.append((w.word, w.flag)) #make every word and tag as a tuple and add them to a list
        return pos_list
    elif para == 'str':
        pos_data2 = jieba.posseg.cut(sentence)
        pos_list2 = []
        for w2 in pos_data2:
            pos_list2.extend([w2.word.encode('utf8'), w2.flag])
        pos_str = ' '.join(pos_list2)
        return pos_str



""" 
Sentence cutting algorithm without bug, but a little difficult to explain why
切割成句子(fix bug after)
"""

def cut_sentence_final(words):
    try:
        #words = (words).decode('utf8')
        start = 0
        i = 0 #i is the position of words
        token = 'meaningless'
        sents = []
        punt_list = ',.!?;~，。！？；～… '.decode('utf8')
        for word in words:
            if word not in punt_list:
                i += 1
                token = list(words[start:i+2]).pop()
                #print token
            elif word in punt_list and token in punt_list:
                i += 1
                token = list(words[start:i+2]).pop()
            else:
                sents.append(words[start:i+1])
                start = i+1
                i += 1
        if start < len(words):
            sents.append(words[start:])
        return sents
    except Exception as e:
        log.logger.error("cut sentences error : "+str(e))
        return ""


'''
    写入excel
'''
import xlutils.copy
import xlwt
def write_excel_data(filepath,sheetnum,stratRow,columnNum,dataSet):
    # w = Workbook()  # 创建一个工作簿
    rb = xlrd.open_workbook(filepath)
    wb = xlutils.copy.copy(rb)
    ws = wb.get_sheet(sheetnum-1)
    for data in dataSet:
        ws.write(stratRow,columnNum,data[0])
        ws.write(stratRow,columnNum+1,data[1])
        stratRow += 1
    # ws.write(0, 0, 'bit')  # 在1行1列写入bit
    # ws.write(0, 1, 'huang')  # 在1行2列写入huang
    # ws.write(1, 0, 'xuan')  # 在2行1列写入xuan
    wb.save(os.path.splitext(filepath)[0] + '_out.xls')  # 保存





if __name__ == "__main__":
    ss = '{"word":"机器学习","jobId":136,"source":"0","userId":1,"time_start":1499914044,"time_end":1500518844,"articles":{"title":"为什么日本的生育率会持续低迷？","time":"2017-07-14 00:55","content":"一周工作60个小时哪有时间处对象","url":"https://www.zhihu.com/question/20461515/answer/198003509","comment":[]}}'
    process_json_data_from_tencnetNews(ss)
    pass
