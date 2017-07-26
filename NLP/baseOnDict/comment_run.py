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
    pool = redis.ConnectionPool(host='10.21.3.127', port=6379, db=0)
    r = redis.Redis(connection_pool=pool)
    while True:
        try:
            # 如果队列为空，那么此处返回一个空数组
            #conda install MySQL-python linux 下安装mysqldb
            # jsonArray = r.lrange("task_comment_scraperlist", -1, -1)
            # TODO 当所有的操作都完成后，并且数据已经正确的处理完毕，可以把redis队列中的key删掉了
            jsonData = r.rpop("task_comment_scraperlist")
            # 这里如果是空数组的话 就是false
            # jsonData = jsonArray[0]
            if jsonData:
                # print jsonData
                '''
                    解析json
                    return (任务ID,话题ID,来源,[评论内容，评论发布时间，点赞数,昵称,头像])
                '''
                one_job = tools.process_json_data_from_comment(jsonData)
                jobId = one_job[0]
                topicId = one_job[1]
                source = one_job[2]
                # print one_job[3].__len__()
                # 获取评论的数组
                comment_list = one_job[3]
                '''
                    计算情感值
                    return : [((topic_title,topic_content,topic_pos,topic_neg,topic_calc_score,topic_time,topic_url),[(comment_content,comment_pos,comment_neg,comment_calc_score,comment_praise_count,comment_time,comment_nick,comment_avatar)])]
                '''
                comments = API.calc_score_for_comment(comment_list, jobId)
                comments_data = []

                for comment in comments:
                    # print到控制台后将unicode转换成中文
                    # print "\n".join(
                    #     [" ".join([str(i).replace('u\'', '\'').decode("unicode-escape") for i in one_topic])])
                    # print comment[0] + "," + str(comment[1]) + "," + str(comment[2]) + "," + str(
                    #     comment[3]) + "," + str(comment[4]) + "," + comment[5]
                    comment_content = comment[0][0:995] + "..." if len(comment[0]) > 1000 else comment[0]
                    comment_score = round(comment[3], 2)
                    # TODO 线上关掉
                    # log.logger.info("comment_score = "+str(comment_score))
                    comments_data.append((comment_content, comment_score, comment[5], topicId, comment[4], jobId, source,
                                         comment[6], comment[7]))
                        # print "\n".join([" ".join([str(i).replace('u\'', '\'').decode("unicode-escape") for i in comments])])
                storeCommentToMysql(False, comments_data)
                print 'comment process success!!!'
        except Exception as e:
            # log.logger.error("process redis data error : " + str(e))
            traceback.print_exc()
        # break

def storeCommentToMysql(isOne, data):
    (conn, cur) = conn_util.createConn()
    # cur.execute("insert into Topic(userId,title,content,happenTime,source) values(2,'AA','BBB','"+tm+"','qq')")
    sqli = "insert into Comment(content,score,publishTime,topic_id,praiseCount,job_id,source,nickName,avatar) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
        if (isOne):
            cur.execute(sqli, data)
        else:
            cur.executemany(sqli, data)
        conn.commit()
    except Exception:
        log.logger.error("insert comment data to mysql error : " + traceback.format_exc())
        # for i in data:
        #     log.logger.error("score = "+str(i[1]))
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
    # pool = redis.ConnectionPool(host='10.21.3.127', port=6379, db=0)
    # r = redis.Redis(connection_pool=pool)
    # a = r.rpop("test111")
    # print a
    # print round(12.1,2)
    pass
