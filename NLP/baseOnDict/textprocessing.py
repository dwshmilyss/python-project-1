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
        #TODO 这里要加上3个值，爬虫写入redis的时候也要加上
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
    aa = projectPath + "/test_dataset/tt.txt"
    # print  os.path.splitext(aa)[1]
    # write_excel_data(aa,1)

    # python27PackagePath1 = os.path.abspath(sys.path[:-1])
    # s = '{"title":"陈羽凡背绿腰包回应白百何出轨：蛋疼的回家过节吧","time":"2017-04-14 02:09","content":"陈羽凡做出闭嘴的手势腾讯娱乐报道 今天凌晨，陈羽凡晒照疑似回应白百何出轨，他晒出自己的照片，并留言：蛋疼的，都回家过节吧。这条微博似乎是在从侧面回应卓伟爆料的白百何私会男模新闻，但直到目前为止，身为事件的当事人白百何至今并未回应此事。有网友评论，哥 ，你被绿了，继一指弹后还出来了个摸臀杀，这样的女人休了！也有网友直言，除了百何的戏和羽凡的歌，别的都与我们无关，与是非曲直无关的人又何谈他人的曲直是非，我喜欢百何的电影，羽凡的音乐，刚好这事与电影和音乐都无关。路人尽量消停点，毕竟百何并没有和你男票出轨，羽凡就算离婚了也应该娶不到各位头上，喜欢就支持，不喜欢也别冒充警察，一个观众的自我修养。","url":"http://news.qq.com/a/20170414/001578.htm?pgv_ref=aio2015&ptlang=2052","comment":[{"time":1492110157,"content":"每当看到哪个明星又分手了，一堆人评论:心疼……一天到晚心疼陈羽凡，心疼丫丫，心疼王宝强，一群刚能吃饱饭的去心疼人家年收入上亿的富豪，你有啥资格心疼人家啊？人家有名气，有钱，你啥也没有，恋爱也没谈过，天天大门不出二门不迈的，抱个破手机就心疼了。还是先疼下自己吧！","up":"53402"},{"time":1492136171,"content":"陈羽凡让白百何红了，白百何让陈羽凡绿了，一段感情就这么黄了。出轨队又得一分，吸毒队和嫖娼队要加油啊！作为近几年最受争议的三个传奇女性，给大家表演个节目吧。白百何 姚笛 马蓉 预备唱：白姚马 腚朝西 驼着王宝强 文章和助理 明星取精很容易 一取就是几万亿 什么冰火鲜肉什么文章助理 什么国外宾馆什么泳池飞机。","up":"1036"},{"time":1492136173,"content":"看到这次的评论，竟然有一半的评论觉得出轨关你什么事。因为对于出轨这件事，大家已经开始麻木了。下一次，再有明星出轨婚外情啊之类，应该就是全民骂媒体干嘛要爆料出来，出轨的人根本就是被害者之类的吧。这就是公众人物的影响力，把大家的三观都扭转了","up":"309"},{"time":1492136327,"content":"其实因感情不合而离婚倒很正常，离婚后再恋爱大家也无可厚非，但是婚内出轨的行为不管是明星还是百姓，都是应该被唾弃的，作为公众人物，肩负着宣传正能量的责任和义务，就跟应该严格约束自己。","up":"383"},{"time":1492136198,"content":"白百何和马蓉正式成立组合了，取名白蓉马，走上取精之路。","up":"335"},{"time":1492121954,"content":"她是演员，可能还是是很多人的标杆，不管认不认她都是公众人物，不管是不是公众人物，出轨错了就是错了！她出轨和很多看客没有关系？也许她就影响着身边差不多的影迷也包括一些孩子。没有感情可以离婚再谈恋爱，可是她还不是为了利益才选择隐瞒而导致今天的？","up":"1164"},{"time":1492136359,"content":"羽哥的意思很明确 我们都曾经做过对不起对方的事……所以 选个绿包 来以此证明 只要顶不绿 包没关系……","up":"104"},{"time":1492135836,"content":"我喜欢百何的电影，羽凡的音乐，刚好这事与电影和音乐都无关。","up":"577"},{"time":1492136534,"content":"这两夫妻说不定早离了，不合适离婚并没什么，但明明离了还欺骗大众天天秀恩爱就是人品问题了。虽然他们确实与我们无关，但作为公众人物你起码得是个正面人物，更要学会尊重大家","up":"221"},{"time":1492108925,"content":"一个观众的修养？更重要的是艺人修养吧！赚着观众的钱还整天净整些没用的负能量！","up":"5145"},{"time":1492135755,"content":"陈羽凡让野白合红了，野白合让陈羽凡绿了，一段感情黄了……","up":"410"},{"time":1492136527,"content":"以前就知道白百合演的电影好看，不知道她叫什么名字，现在知道了，这广告打的值。","up":"33"},{"time":1492136441,"content":"二十年前罗大佑专门为此事写下不朽的歌谣，《野百合也有春天》","up":"71"},{"time":1492136368,"content":"永远喜欢，人生的路上没有一个人是不做错事的。明星也是普通的人，也会做错事。在说了任何事都是两面的，任何错误也不应该一个人承担。","up":"15"},{"time":1492108572,"content":"作为公众人物，她就是错了。拿着天价的报酬，人前装少女。骗得观众对她爱。人后却是欲女。","up":"18951"},{"time":1492108961,"content":"一个戏子玩玩鸭子，关你半毛钱的事。玩鸭子的费用还是你们进电影院帮忙凑的","up":"33317"},{"time":1492110450,"content":"如果已经离婚了就公布吧！如果还没离婚别那么骚吧！在大庭广众之下别干出那么龌龊的事！实在熬不住！回家去搞！別丢你儿子的脸。。。","up":"11468"},{"time":1492108438,"content":"这个沙发冷清得太讽刺～唉～娱乐圈～除了戏子～真正的的艺术家屈指可数啊～","up":"6082"},{"time":1492108140,"content":"我可以听陈羽凡的歌，更可以不看白百何的戏，出轨了没什么好说，尤其是女人！","up":"1651"},{"time":1492113075,"content":"陈羽凡还是很想的开的？就当自行车丢了？让别人骑一圈又送回来了？还能使？呵呵！想开点长寿？","up":"3561"},{"time":1492108909,"content":"自己的东西让人用过了，感觉没面子扔了，然后又从新选一个别人用过的东西，这样就觉得有面子多了😀😀😀这就叫真爱？","up":"3327"},{"time":1492108749,"content":"哎，看了陈羽凡发这照片有点这种意思：“你们关注他老婆这事的都是闲得蛋疼！闭嘴，都回去的些。”","up":"3781"},{"time":1492109619,"content":"娱乐圈是最肮脏的圈子！比如，张柏芝脱光了掰开给陈冠希拍照，现在跟没事人一样！在比如，关之琳和富豪往下面塞高尔夫球，拿不出来，半夜去医院，还塞两个！现在还是屏幕面前人五人六的装纯！你说他们得有多厚的脸皮啊！","up":"2180"},{"time":1492108311,"content":"这样的女人还要？真留来过节啊？娱乐圈人果然是够胸襟 绿了无所谓最主要是钱钱钱💰","up":"1135"},{"time":1492108507,"content":"这话应该说爆料者，关你们屌事呀，你们在七嘴八舌，我都没在乎你们在乎什么！好笑。","up":"1569"},{"time":1492111593,"content":"很正常啊，男人女人哪个人不是骚浪贱？只是遇没遇到让你露出狐狸尾巴的那个人。不要刻薄的只说别人的不是，有一天却自扇嘴巴。人生的路还长着呢，谁也看不到自己的明天，请各位嘴上留德。毕竟是人家的事与群众无关，看看热闹得了。","up":"1415"},{"time":1492117469,"content":"我来替楼主表达下意思，传统中国封建思想，好比1-男人赤膊女人怎么了就不能赤膊了嘛？你会赤膊吗？2-男人站路边尿尿了女人怎么了就不能路边尿尿吗？3-自己家里有男人和别的女人睡了你心里会想没撒吃亏的要是女人生被人家睡了至少你的心是沉重的，等等好多比方男女都无法平等有些思想跟深蒂固。仅代表个人看法不支持任何一方！","up":"483"},{"time":1492109005,"content":"对呀，人家自己的事别人何必操心，都是闲的……再说人家的婚烟愿意怎么过就怎么过！桌啥来着你这真是没事闲的蛋疼！","up":"702"},{"time":1492112253,"content":"哈哈、、人家说你们呢，蛋疼的，回家过节吧，人家两夫妻就喜欢这样。关你们啥事","up":"600"},{"time":1492121965,"content":"作为公众人物，她就是错了。拿着天价的报酬，人前装少女。骗得观众对她爱。人后却是欲女。","up":"265"},{"time":1492122772,"content":"人都有七情六欲，毕竟都是动物。有的人清洁挂的高高在上，可以出家了，何必在评论里说别人是非。蛋疼的，回家过节吧。","up":"397"},{"time":1492108181,"content":"大神们你好，我是新来的，不懂规矩，我就想问，我是直接喷？还是排队喷？愚人节过了吧！今天几号啦！","up":"321"},{"time":1492108737,"content":"喜欢文末的这段话，除了百合的戏和羽凡的歌，别的都与我们无关，与是非曲直无关的人又何谈他人的曲直是非，我喜欢百合的电影，羽凡的音乐，刚好这事与电影和音乐都无关。路人尽量消停点，毕竟百合并没有和你男票出轨，羽凡就算离婚了也应该娶不到各位头上，喜欢就支持，不喜欢也别冒充警察，一个观众的自我修养。","up":"140"},{"time":1492109590,"content":"其实娱乐圈好多离婚的，为了利益没公开而已，像孙俪和邓超，大家都以为他俩很恩爱，都是假象，早就离了，没办法，为了利益必须得演啊，不然就名誉扫地，搞不好还会破产，为了继续圈钱而已。","up":"58"},{"time":1492121922,"content":"第二个王宝强。只要把钱袋子扣紧了没事演艺圈找个老婆超过她的遍地都是。","up":"61"},{"time":1492108800,"content":"这种事就跟美日自己划的那个封锁咱们的岛链一样，多过几次也就习惯了。。这年头谁还没看过别人家的老公老婆出轨啊，明星出轨多个啥啊？多看几次也就习惯了。。多大点屁事儿。","up":"196"},{"time":1492115353,"content":"管人家一点破事干嘛！放下手机走出卫生间看看自已女人还在不在床上吧，不要让隔壁你姓王的朋友抱走了你都不知道。","up":"139"},{"time":1492121898,"content":"好与不好跟每个人都无关！管理好自己才是真事！吵吵闹闹的音乐、搬搬的演技！干嘛那么激动！又不付钱！给予！省省力气吧！各吃各的饭吧！","up":"38"},{"time":1492132173,"content":"羽凡已经很明确表示原谅百何或不在意百何的出轨行为，也非常明确表示各位看客不要围观，在这一对明星眼里只有永恒利益，没有永恒爱情，一旦离了，对小孩是伤害，更对财产分配问题会有严重分歧化，与其这样还不如各玩各的！😊","up":"9"},{"time":1492131247,"content":"毕竟她是公众人物，所以跟我们有关系啊 不然她的电影不看了 什么广告牌商品全部买，你们说有没有关系","up":"3"},{"time":1492132801,"content":"我从来不追星，遇到了，看看，好像，他们吃香的喝辣的，从来没关注我们面朝黄土背朝天的人，而我们这些人，自己家的油盐酱醋茶，都备不齐。。。想想，我们是不是，没事找事，不嫌事多。。。","up":"7"},{"time":1492121896,"content":"娱乐圈混乱圈子，出轨很正常！多少没被潜规则过！都是二手货了，结婚10来年了换换口味，人家有钱玩得起，人家都不要脸，你们操那心干嘛！","up":"17"},{"time":1492125349,"content":"无聊的脑残粉，有这时间好好工作，陪陪家人，做点有意义的事不好吗，成天看热闹不嫌事大，跟你有啥关系？人家少块肉还是掉块骨头了？中国最脑残的就是粉丝，一月不吃不喝省吃俭用吃泡面也得维护明星，给明星刷礼物","up":"10"},{"time":1492130484,"content":"路人尽量消停点，毕竟百何并没有和你男票出轨，羽凡就算离婚了也应该娶不到各位头上，喜欢就支持，不喜欢也别冒充警察，一个观众的自我修养。","up":"2"},{"time":1492121745,"content":"就想问下“卓伟”，你没有犯过错？你自己就真的超凡脱俗，不食人间烟火？人家两人的婚姻关你鸟事？“宁拆十座庙不毁一段姻缘”懂不懂啊？就烦这样的狗仔，拆散一对是一对，是吧？人家离了对你有什么好处？还是借题想出名？你不喜欢羽凡的歌？没看过百合的电影？还是出于羡慕嫉妒恨的私心呢？","up":"28"},{"time":1492134168,"content":"哎，人家夫妻都无所谓，这些网友不知道在激动个啥。有这闲情，还不如回家苦力上班多挣钱，少让你未来老婆在别人那挨点炮。","up":"1"},{"time":1492121962,"content":"这意思很明确啊:你们都闲得蛋疼，尼玛，我们早就离婚了，想跟哪个玩就跟哪个玩^O^","up":"6"},{"time":1492115269,"content":"陈思诚、陈赫、刘恺威、林丹可以拍部电影,文章当导演,徐峥当出品人,白百合、王鸥、马蓉、张子萱、姚迪演女主角,陶喆和汪峰来唱主题曲,卓伟老师来当发行。","up":"39"},{"time":1492130239,"content":"一群闲得蛋疼的玩意，别人出轨跟你们有半分钱关系啊！死了都跟我没关系！","up":"4"},{"time":1492125350,"content":"为什么男人找小三就不说呢，而女人有点屁大的事就搞的好像犯了多大事似的，如果她老公对她好她会跟别的男人在一起吗，说不定人家两口早就离婚了呢","up":"11"}]}'.decode("utf8")
    # aa = json.loads(s)
    # # print aa['title']
    # print len(aa['comment'])

    get_input_data_from_qq(projectPath + "/test_dataset/haha_bak.txt")
    pass
