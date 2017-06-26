#!/usr/bin/env python
# encoding: utf-8

import sys
import pos_neg_senti_dict_feature as API
import textprocessing as tools
import redis

"""
主程序运行入口
@version: v1.0
@author: dww
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: run.py
@time: 2017/4/13 15:29
"""
import log
import MySQLdb
import traceback
import conn_util


# #################################################################################################
# '''配置log'''
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


def getRedisData():
    try:
        pool = redis.ConnectionPool(host='10.21.3.127', port=6379, db=0)
        r = redis.Redis(connection_pool=pool)
        # while True:
        # 如果队列为空，那么此处返回一个空数组
        jsonArray = r.lrange("taskscraperlist", -1, -1)
        # 这里如果是空数组的话 就是false
        if jsonArray:
            jsonData = jsonArray[0]
            # print jsonData
            '''
                解析json
                return (查询关键词，开始时间，结束时间，JOB_ID，USER_ID，来源，[((话题标题，话题发布时间，话题内容，原文链接),[评论内容，评论发布时间，点赞数，昵称，头像])...])
                这里需要再加上一个originUrl(原文链接)
            '''
            one_job = tools.process_json_data_from_tencnetNews(jsonData)
            keyWord = one_job[0]  # 关键词
            jobId = one_job[3]  # JOB ID
            source = one_job[5]
            # print one_job[3].__len__()
            topic_list = one_job[4]
            '''
                计算情感值
                return : [((topic_title,topic_content,topic_pos,topic_neg,topic_calc_score,topic_time,topic_url),[(comment_content,comment_pos,comment_neg,comment_calc_score,comment_praise_count,comment_time,comment_nick,comment_avatar)])]
            '''
            topics = API.calc_score_for_tencentNews(topic_list, jobId)
            topic_list = []
            comment_list = []

            for one_topic in topics:
                # print到控制台后将unicode转换成中文
                print "\n".join(
                    [" ".join([str(i).replace('u\'', '\'').decode("unicode-escape") for i in one_topic])])
                topic = one_topic[0]
                # 超过数据库字段长度要截取[0:250]从0截取到250(不包含250)
                topic_title = topic[0][0:250] + "..." if len(topic[0]) > 255 else topic[0]
                topic_content = topic[1][0:995] + "..." if len(topic[1]) > 1000 else topic[1]

                # print "len = "+str(len(topic[0]))
                # print topic[0] + "," + topic[1] + "," + str(topic[2]) + "," + str(topic[3]) + "," + str(
                #     topic[4]) + "," + topic[5]
                topic_id = storeTopicToMysql(True, (jobId, topic_title, topic_content, topic[5], source, topic[4]),
                                             topic[6])
                # topic_list.append((jobId, topic[0], topic[1], topic[5], "qq", topic[4]))
                comments = one_topic[1]
                for comment in comments:
                    # print comment[0] + "," + str(comment[1]) + "," + str(comment[2]) + "," + str(
                    #     comment[3]) + "," + str(comment[4]) + "," + comment[5]
                    comment_content = comment[0][0:995] + "..." if len(comment[0]) > 1000 else comment[0]
                    comment_list.append((comment_content, comment[3], comment[5], topic_id, comment[4], jobId, source,
                                         comment[6], comment[7]))
                    # print "\n".join([" ".join([str(i).replace('u\'', '\'').decode("unicode-escape") for i in comments])])
                storeCommentToMysql(False, comment_list)
                comment_list = []
                # TODO 当所有的操作都完成后，并且数据已经正确的处理完毕，可以把redis队列中的key删掉了
                # r.rpop("taskscraperlist")
        else:
            # print "aaa"
            log.logger.warning("data from redis is empty!!!")

    except Exception as e:
        # log.logger.error("process redis data error : " + str(e))
        traceback.print_exc()
        pass


def storeToMysql():
    conn = MySQLdb.connect(
        host='10.21.3.120',
        port=3306,
        user='root',
        passwd='wenha0',
        db='yiban_BI',
    )
    cur = conn.cursor()
    cur.execute("insert into test_person(name,age) values('Tom2',10)")
    cur.close()
    # conn.commit()
    conn.close()
    pass


def storeTopicToMysql(isOne, data):
    (conn, cur) = conn_util.createConn()
    # cur.execute("insert into Topic(userId,title,content,happenTime,source) values(2,'AA','BBB','"+tm+"','qq')")
    sqli = "insert into Topic(job_id,title,content,publishTime,source,score) values (%s,%s,%s,%s,%s,%s)"
    id = 0
    try:
        if (isOne):
            cur.execute(sqli, data)
            id = int(conn.insert_id())
            # 在solr中建立索引
            from SolrUtil import MySolrPy

            # 连接数据库
            msp = MySolrPy('http://localhost:8080/solr/test')
            bean = {
                'id': id,
                'jobId': data[0],
                'title': data[1],
                'content': data[2],
            }
            msp.add(bean)
            msp.commit()
        else:
            cur.executemany(sqli, data)
        conn.commit()
    except Exception:
        log.logger.error("id = " + str(id) + ",insert topic data to mysql error : " + traceback.format_exc())
        conn.rollback()
    conn_util.closeConn(conn, cur)
    return id


def storeCommentToMysql(isOne, data):
    (conn, cur) = conn_util.createConn()
    # cur.execute("insert into Topic(userId,title,content,happenTime,source) values(2,'AA','BBB','"+tm+"','qq')")
    sqli = "insert into Comment(content,score,publishTime,topic_id,praiseCount,job_id,source) values (%s,%s,%s,%s,%s,%s,%s)"
    try:
        if (isOne):
            cur.execute(sqli, data)
        else:
            cur.executemany(sqli, data)
        conn.commit()
    except Exception:
        log.logger.error("insert comment data to mysql error : " + traceback.format_exc())
        conn.rollback()
    conn_util.closeConn(conn, cur)


if __name__ == "__main__":
    # if len(sys.argv) < 3:
    #     print 'No action specified.'
    #     sys.exit()
    # type = sys.argv[1]
    # if type == "content":
    #     print tools.single_review_sentiment_score(sys.argv[2].decode("utf8"))
    # elif type == "file":
    #     pass

    getRedisData()
    # storeTopicToMysql1()

    pass
