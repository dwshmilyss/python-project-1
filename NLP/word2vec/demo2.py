#!/usr/bin/env python
# encoding: utf-8
import MySQLdb


def storeToMysql():
    conn = MySQLdb.connect(
        host='10.21.3.120',
        port=3306,
        user='root',
        passwd='wenha0',
        db='yiban_BI',
    )
    cur = conn.cursor()
    conn.set_character_set('utf8')
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')
    s = u'这些名字，习近平从未'
    cur.execute("insert into test_person(name,age) values('"+s+"',100)")
    conn.commit()
    print "ID of last record is ", int(cur.lastrowid)  # 最后插入行的主键ID
    print "ID of inserted record is ", int(conn.insert_id())  # 最新插入行的主键ID，conn.insert_id()一定
    cur.close()
    conn.close()
    pass


import time


# 时间戳转格式化字符串
def timeStamp_transform_str(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime


# 格式化时间字符串
def str_transform_format_str(timeStr):
    # tm = "2013-10-10 23:40:00"
    # timeArray = time.strptime(timeStr,"%Y-%m-%d %H:%M:%S")
    # 这里的格式一定要严格的对应到原字符串的格式
    # tm = "2013-10-10 23:40"
    timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M")
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M", timeArray)
    return otherStyleTime


def storeToMysql1():
    conn = MySQLdb.connect(
        host='10.21.3.120',
        port=3306,
        user='root',
        passwd='wenha0',
        db='test',
    )
    str1 = "2013-10-13 23:40"
    str2 = "2013-10-13 23:40"
    str3 = "2013-10-14 23:40"
    tm1 = str_transform_format_str(str1)
    tm2 = str_transform_format_str(str2)
    tm3 = str_transform_format_str(str3)
    cur = conn.cursor()
    # sqli = "insert into student values(%s,%s,%s,%s)"
    # cur.execute(sqli, ('3', 'Huhu', '2 year 1 class', '7'))

    # cur.execute("insert into Topic(userId,title,content,happenTime,source) values(2,'AA','BBB','"+tm+"','qq')")

    sqli = "insert into Topic(userId,title,content,publishTime,source) values (%s,%s,%s,%s,%s)"
    cur.executemany(sqli, [
        (3, 'Tom', '1 year 1 class', tm1, 'qq'),
        (4, 'Jack', '2 year 1 class', tm2, 'qq'),
        (6, 'Yaheng', '2 year 2 class', tm3, 'qq')

    ])

    cur.close()
    conn.commit()
    conn.close()
    pass


def test():
    try:
        arr = []
        1 / 0
        arr.append(1)
    except Exception as e:
        print e
    return arr

import json



if __name__ == "__main__":
    # storeToMysql()
    # x = 1
    # print (x == 1 and "True") or "False"
    # print "Fire" if True else "Water"
    # s = '01234'
    # print s[0:3]

    map = {}
    arr = ["a","b","a","b","c","a"]
    for i in arr:
        if i not in map.keys():
            map[i] = 1
        else:
            map[i] = map[i] + 1
    a = sorted(map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)[0:2]
    print a
    jsonStr = json.dumps(a, ensure_ascii=False, encoding='UTF-8')
    print jsonStr
    # for (k, v) in map.items():
    #     print "dict[%s] =" % k, v
    pass
