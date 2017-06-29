#! /usr/bin/env python2.7
# coding=utf-8

import numpy as np
import textprocessing as tp
import sys
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import traceback

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
import os

import MySQLdb
import traceback
import conn_util
import json

'''定义工程所在目录路径'''
projectPath = os.path.abspath(os.path.dirname(sys.argv[0]))

'''加载词典 start'''
'''加载情感词典 start'''
#正情感词典(自定义)
posDictPath = projectPath + "/../sentiment_dictionary/positive_dictionary/sentiment/posdict.txt"
posDictData = tp.get_txt_data(posDictPath, "lines")
# 正情感词典(台湾大学)
ntusdPosDictPath = projectPath + "/../sentiment_dictionary/positive_dictionary/sentiment/ntusd-positive.txt"
ntusdPosDictData = tp.get_txt_data(ntusdPosDictPath, "lines")
# 正情感词典(清华大学)
tsinghuaPosDictPath = projectPath + "/../sentiment_dictionary/positive_dictionary/sentiment/tsinghua_positive_gb.txt"
tsinghuaPosDictData = tp.get_txt_data(tsinghuaPosDictPath, "lines")
# 正情感词典(知网)
hownetPosDictPath = projectPath + "/../sentiment_dictionary/positive_dictionary/sentiment/hownet_positive_sentiment_cn.txt"
hownetPosDictData = tp.get_txt_data(hownetPosDictPath, "lines")
#合并
posSentimentDictData_all = set(posDictData + ntusdPosDictData + tsinghuaPosDictData + hownetPosDictData)

# 负情感词典(自定义)
negDictPath = projectPath + "/../sentiment_dictionary/negative_dictionary/sentiment/negdict.txt"
negDictData = tp.get_txt_data(negDictPath, "lines")
# 负情感词典(台湾大学)
ntusdNegDictPath = projectPath + "/../sentiment_dictionary/negative_dictionary/sentiment/ntusd-negative.txt"
ntusdNegDictData = tp.get_txt_data(ntusdNegDictPath, "lines")
# 负情感词典(清华大学)
tsinghuaNegDictPath = projectPath + "/../sentiment_dictionary/negative_dictionary/sentiment/tsinghua_negative_gb.txt"
tsinghuaNegDictData = tp.get_txt_data(tsinghuaNegDictPath, "lines")
# 正情感词典(知网)
hownetNegDictPath = projectPath + "/../sentiment_dictionary/negative_dictionary/sentiment/hownet_negative_sentiment_cn.txt"
hownetNegDictData = tp.get_txt_data(hownetNegDictPath, "lines")
#合并并去重
negSentimentDictData_all = set(negDictData + ntusdNegDictData + tsinghuaNegDictData + hownetNegDictData)
'''加载情感词典 end'''


'''加载评价词典 start'''
#正面评价词典（知网）
posEvaCNDictPath_1 = projectPath + "/../sentiment_dictionary/positive_dictionary/evaluation/hownet_positive_evaluation_cn_1.txt"
posEvaCNDictData_1 = tp.get_txt_data(posEvaCNDictPath_1, "lines")
posEvaCNDictPath_2 = projectPath + "/../sentiment_dictionary/positive_dictionary/evaluation/hownet_positive_evaluation_cn_2.txt"
posEvaCNDictData_2 = tp.get_txt_data(posEvaCNDictPath_2, "lines")
posEvaCNDictPath_3 = projectPath + "/../sentiment_dictionary/positive_dictionary/evaluation/hownet_positive_evaluation_cn_3.txt"
posEvaCNDictData_3 = tp.get_txt_data(posEvaCNDictPath_3, "lines")
#合并并去重
posEvaluationDictData_all = set(posEvaCNDictData_1 + posEvaCNDictData_2 + posEvaCNDictData_3)

'''合并正情感词典和正评价词典'''
posDictDataAll = set(posSentimentDictData_all | posEvaluationDictData_all)

#负面评价词典
negEvaCNDictPath = projectPath + "/../sentiment_dictionary/negative_dictionary/evaluation/hownet_negative_evaluation_cn.txt"
negEvaCNDictData = tp.get_txt_data(negEvaCNDictPath, "lines")

'''合并负情感词典和正评价词典'''
negDictDataAll = set(negSentimentDictData_all | set(negEvaCNDictData))

'''加载评价词典 end'''


'''加载程度副词词典 start'''
# “极其|extreme / 最|most”
mostDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/most.txt"
mostDictData = tp.get_txt_data(mostDictPath, 'lines')

# “很|very”
veryDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/very.txt"
veryDictData = tp.get_txt_data(veryDictPath, 'lines')

# “较|more”
moreDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/more.txt"
moreDictData = tp.get_txt_data(moreDictPath, 'lines')

# “稍|-ish”
ishDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/ish.txt"
ishDictData = tp.get_txt_data(ishDictPath, 'lines')

# “欠|insufficiently”
insufficientlyDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/insufficiently.txt"
insufficientlyDictData = tp.get_txt_data(insufficientlyDictPath, 'lines')

# “超|over”
overDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/over.txt"
overDictData = tp.get_txt_data(overDictPath, 'lines')

# 否定词语
inverseDictPath = projectPath + "/../sentiment_dictionary/adverbs_of_degree_dictionary/inverse.txt"
inverseDictData = tp.get_txt_data(inverseDictPath, 'lines')
'''加载程度副词词典 end'''
'''加载词典 end'''




# 2. Sentiment dictionary analysis basic function
# Function of matching adverbs of degree and set weights
# 强度从高到低赋予权重 : most > very > more > ish > insufficient > inverse
# 除了inverse为负面，其他都是正面的
def match(word, sentiment_value):
    if word in mostDictData:
        sentiment_value *= 2.0
    elif word in overDictData:
        sentiment_value *= 1.75
    elif word in veryDictData:
        sentiment_value *= 1.5
    elif word in moreDictData:
        sentiment_value *= 1.25
    elif word in ishDictData:
        sentiment_value *= 0.5
    elif word in insufficientlyDictData:
        sentiment_value *= 0.25
    elif word in inverseDictData:
        sentiment_value *= -1
    return sentiment_value


# Function of transforming negative score to positive score
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
    pos_count = 0
    neg_count = 0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return [pos_count, neg_count]


'''计算得分 格式：[Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]'''
def sumup_sentence_sentiment_score(score_list_byId):
    try:
        score_array = np.array(score_list_byId)  # Change list to a numpy array
        # sum求和
        # 第一列为正情感分
        Pos = np.sum(score_array[:, 0])  # Compute positive score
        # 第二列为负情感分
        Neg = np.sum(score_array[:, 1])

        # 求均值
        AvgPos = np.mean(score_array[:, 0])  # Compute review positive average score, average score = score/sentence number
        AvgNeg = np.mean(score_array[:, 1])

        # 求标准差
        StdPos = np.std(score_array[:, 0])  # Compute review positive standard deviation score
        StdNeg = np.std(score_array[:, 1])
        return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]
    except Exception as e:
        log.logger.error("sumup sentence sentiment score error : "+str(e))
        return None



'''
    输入一段文本，切割成句子后计算每个句子的情感值
    :parameter review : 一段文本
    :return : [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]
'''
def calc_single_sentiment_score(review):
    wordMap = {}
    #判断文本内容是否为空
    if review is not None and review.strip() != "":
        single_review_senti_score = []
        review_sentiment_score = []
        #切成句子的数组
        cuted_review = tp.cut_sentence_final(review)

        # 遍历每一个句子
        for sent in cuted_review:
            try :
                if sent is not None and sent != '':
                    # 分词
                    seg_sent = tp.segmentation(sent, 'list')
                    i = 0  # word position counter
                    s = 0  # sentiment word position
                    poscount = 0  # count a positive word
                    negcount = 0  # count a negative word
                    pos_max = 1000
                    neg_max = 1000

                    # 遍历句子中的每一个词
                    for word in seg_sent:
                        if word not in wordMap.keys():
                            wordMap[word] = 1
                        else:
                            wordMap[word] = wordMap[word] + 1

                        # 如果该词在正情感词典中
                        if word in posDictDataAll:
                            # 正情感分+1
                            poscount += 1
                            for w in seg_sent[s:i]:
                                poscount = pos_max if round(match(w, poscount),2) > pos_max else round(match(w, poscount),2)
                            a = i + 1

                        elif word in negDictDataAll:
                            negcount += 1
                            for w in seg_sent[s:i]:
                                negcount = neg_max if round(match(w, negcount),2) > neg_max else round(match(w, negcount),2)
                            a = i + 1

                        # Match "!" in the review, every "!" has a weight of +2
                        elif word == "！".decode('utf8') or word == "!".decode('utf8'):
                            for w2 in seg_sent[::-1]:
                                if w2 in posDictData:
                                    poscount += 2
                                    break
                                elif w2 in negDictData:
                                    negcount += 2
                                    break
                        i += 1

                    # 将每个句子的正负情感分规约后放入List 格式：[句子,[pos,neg]]
                    single_review_senti_score.append(transform_to_positive_num(poscount, negcount))
            except Exception as e:
                log.logger.error('process json data of tencent news error : ' + str(e))
        # 利用Numpy对二维数组中的列进行统计 求和、均值、标准差
        review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)
        return (review_sentiment_score[0], review_sentiment_score[1],wordMap)
    else:
        return (0,0,wordMap)



import time
#时间戳转格式化字符串
def timeStamp_transform_str(timeStamp):
    try:
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        return otherStyleTime
    except Exception as e:
        log.logger.error('timestamp transform to string error : ' + str(e))
    return time.strftime("%Y-%m-%d %H:%M",time.localtime(time.time()))

#格式化时间字符串
def str_transform_format_str(timeStr):
    try:
        # tm = "2013-10-10 23:40:00"
        # timeArray = time.strptime(timeStr,"%Y-%m-%d %H:%M:%S")
        #这里的格式一定要严格的对应到原字符串的格式
        # tm = "2013-10-10 23:40"
        timeArray = time.strptime(timeStr,"%Y-%m-%d %H:%M")
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
        return otherStyleTime
    except Exception as e:
        log.logger.error('fromat time error : ' + str(e))
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))


'''
    处理爬取到的news.qq.com数据，计算情感值
    文本数据格式：[((topic_title,topic_time,topic_content,topic_url),[(comment_content,comment_time,comment_praise_count,comment_nick,comment_avatar),...]),...]
    return : [((topic_title,topic_content,topic_pos,topic_neg,topic_calc_score,topic_time,topic_url),[(comment_content,comment_pos,comment_neg,comment_calc_score,comment_praise_count,comment_time,comment_nick,comment_avatar)])]
'''
def calc_score_for_tencentNews(topic_list,jobId):
    try:
        sumMap = {}
        all_topic_res = []
        one_topic_comment_res = []
        #遍历所有话题
        for topic in topic_list:
            '''
                计算topic的情感分(利用topic的content)
            '''
            (topic_title, topic_time, topic_content,topic_url) = topic[0]
            #计算话题的内容情感分
            (topic_pos,topic_neg,map1) = calc_single_sentiment_score(topic_content)
            #统计词频
            for k, v in map1.iteritems():
                if len(k) > 1:
                    if k in sumMap.keys():
                        sumMap[k] = sumMap[k] + v
                    else:
                        sumMap[k] = v
            #一个topic的计算结果
            temp_topic_time = (str_transform_format_str(topic_time) if topic_time else time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())))
            one_topic_res = (topic_title,topic_content,topic_pos,topic_neg,topic_pos - topic_neg,temp_topic_time,topic_url)
            #一个话题评论的情感分计算结果
            for comment in topic[1]:
                # 计算一个评论的内容的得分
                (comment_pos,comment_neg,map2) = calc_single_sentiment_score(comment[0])
                # 统计词频
                for k, v in map2.iteritems():
                    if len(k) > 1:
                        if k in sumMap.keys():
                            sumMap[k] = sumMap[k] + v
                        else:
                            sumMap[k] = v
                #因为有点赞数，所以把点赞数作为系数*情感值
                comment_praise_count = int(comment[2])#点赞数
                comment_nick = comment[3]
                comment_avatar = comment[4]
                #如果时间为空 就给定一个默认值
                temp_comment_time = (timeStamp_transform_str(comment[1]) if comment[1] else time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())))
                comment_score = (comment_pos - comment_neg)*comment_praise_count
                #TODO 线上关掉
                log.logger.info(comment[0]+",comment_pos = "+str(comment_pos)+",comment_neg = "+str(comment_neg)+",comment_praise_count = "+str(comment_praise_count)+",comment_score = "+str(comment_score))
                one_topic_comment_res.append((comment[0],comment_pos,comment_neg,comment_score,comment_praise_count,temp_comment_time,comment_nick,comment_avatar))
            all_topic_res.append((one_topic_res,one_topic_comment_res))
            one_topic_comment_res = []
        #去除中英文的感叹号(在停用词里并没有过滤感叹号，因为感叹号参与了情感值的计算)
        if sumMap.has_key(u'！'):
            print '！'
            del sumMap[u'！']
        if sumMap.has_key('!'):
            del sumMap['!']
            print '!'
        #循环完成后对map的value按降序排序，并截取前20
        arr = sorted(sumMap.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[0:20]
        #转换成json字符串
        # data = json.dumps(arr, ensure_ascii=False, encoding='UTF-8')
        # data = json.dumps(arr, ensure_ascii=False)
        wc_res = []
        #存入mysql
        for temp in arr:
            wc_res.append((jobId,temp[0],temp[1]))
        storeWordCloudToMysql(wc_res)
        #存入数据库
    except Exception as e:
        # log.logger.error("process redis data error : "+str(e))
        traceback.print_exc()
    return  all_topic_res

def storeWordCloudToMysql(data):
    (conn,cur) = conn_util.createConn()
    sqli = "insert into WordCloud(job_id,word,cn) values(%s,%s,%s)"
    try:
        cur.executemany(sqli, data)
        conn.commit()
    except Exception:
        log.logger.error("insert WordCloud data to mysql error : " + traceback.format_exc())
        conn.rollback()
    conn_util.closeConn(conn, cur)

if __name__ == "__main__":
    str = u"我害怕了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还缪了还………无聊"
    a = calc_single_sentiment_score(str)
    print a
    pass