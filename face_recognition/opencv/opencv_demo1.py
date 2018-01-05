#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: opencv_demo1.py
@time: 2018/1/3 13:10
"""
import sys
import cv2
import os
from PIL import Image as image,ImageDraw as imageDraw
cv2.__version__

default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def func():
    pass


class Main():
    def __init__(self):
        pass

'''
测试方法  检测人脸
'''
def test1():
    img = cv2.imread("images/4.jpg")
    cv2.imshow("1",img)

    faceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_default_gpu.xml')
    objImage = cv2.imread("images/4.jpg")
    cvtImage = cv2.cvtColor(objImage, cv2.COLOR_BGR2GRAY)
    foundFaces=faceClassifier.detectMultiScale(cvtImage,scaleFactor=1.1,minNeighbors=9,minSize=(50,50),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    print(" 在图片中找到了 {} 个人脸".format(len(foundFaces)))
    for (x, y, w, h) in foundFaces:
        cv2.rectangle(objImage, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.imshow(u'面部识别的结果已经高度框出来了。按任意键退出'.encode('gb2312'), objImage)
    cv2.waitKey(0)

'''
检测人脸
'''
def detectFaces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # if img.ndim == 3:
    #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # else:
    #     gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,minSize=(30, 30),flags = cv2.cv.CV_HAAR_SCALE_IMAGE)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    result = []
    for (x,y,width,height) in faces:
        result.append((x,y,x+width,y+height))
    return result

'''
保存检测到的人脸
'''
def saveFaces(image_name):
    faces = detectFaces(image_name)
    if faces:
        #将人脸保存在save_dir目录下。
        #Image模块：Image.open获取图像句柄，crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
        save_dir = image_name.split('.')[0]+"_faces"
        os.mkdir(save_dir)
        count = 0
        for (x1,y1,x2,y2) in faces:
            file_name = os.path.join(save_dir,str(count)+".jpg")
            image.open(image_name).crop((x1,y1,x2,y2)).save(file_name)
            count+=1

#在原图像上画矩形，框出所有人脸。
#调用Image模块的draw方法，Image.open获取图像句柄，ImageDraw.Draw获取该图像的draw实例，然后调用该draw实例的rectangle方法画矩形(矩形的坐标即
#detectFaces返回的坐标)，outline是矩形线条颜色(B,G,R)。
#注：原始图像如果是灰度图，则去掉outline，因为灰度图没有RGB可言。drawEyes、detectSmiles也一样。
def drawFaces(image_path):
    faces = detectFaces(image_path)
    if faces:
        img = image.open(image_path)
        draw_instance = imageDraw.Draw(img)
        for (x1,y1,x2,y2) in faces:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(255, 0,0))
        image_name = image_path[find_last(image_path, '/') + 1:]
        image_dir = image_path[0:find_last(image_path, '/') + 1]
        print image_name + ' ' + image_dir
        print image_dir+'drawfaces_'+image_name
        img.save(image_dir+'drawfaces_'+image_name)

'''
查找最后一个字符串出现的位置
'''
def find_last(source_str, target_str):
    last_position=-1
    while True:
        position=source_str.find(target_str, last_position + 1)
        if position==-1:
            return last_position
        last_position=position


'''
眼睛检测
'''
def detectEyes(image_name):
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    # eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    faces = detectFaces(image_name)

    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = []
    for (x1,y1,x2,y2) in faces:
        roi_gray = gray[y1:y2, x1:x2]
        # eyes = eye_cascade.detectMultiScale(roi_gray,1.3,2)
        eyes = eye_cascade.detectMultiScale(roi_gray,scaleFactor=1.3, minNeighbors=2)
        for (ex,ey,ew,eh) in eyes:
            result.append((x1+ex,y1+ey,x1+ex+ew,y1+ey+eh))
    return result

'''
框出眼睛
'''
def drawEyes(image_path):
    faces = detectEyes(image_path)
    if faces:
        img = image.open(image_path)
        draw_instance = imageDraw.Draw(img)
        for (x1,y1,x2,y2) in faces:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(0, 0, 255))
        image_name = image_path[find_last(image_path, '/') + 1:]
        image_dir = image_path[0:find_last(image_path, '/') + 1]
        print image_name + ' ' + image_dir
        print image_dir+'draweyes_'+image_name
        img.save(image_dir+'draweyes_'+image_name)

'''
笑脸检测
'''
def detectSmiles(image_name):
    img = cv2.imread(image_name)
    smiles_cascade = cv2.CascadeClassifier("haarcascade_smile.xml")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    smiles = smiles_cascade.detectMultiScale(gray,4,5)
    result = []
    for (x,y,width,height) in smiles:
        result.append((x,y,x+width,y+height))
    return result

'''
框出笑脸
'''
def drawSmiles(image_path):
    Smiles = detectSmiles(image_path)
    if Smiles:
        img = image.open(image_path)
        draw_instance = imageDraw.Draw(img)
        for (x1,y1,x2,y2) in Smiles:
            draw_instance.rectangle((x1,y1,x2,y2), outline=(100, 100, 0))
        image_name = image_path[find_last(image_path, '/') + 1:]
        image_dir = image_path[0:find_last(image_path, '/') + 1]
        print image_name + ' ' + image_dir
        print image_dir+'drawsmiles_'+image_name
        img.save(image_dir+'drawsmiles_'+image_name)

if __name__ == "__main__":
    # saveFaces("images/6.jpg")
    # drawFaces("images/6.jpg")
    # drawEyes("images/6.jpg")
    drawSmiles("images/6.jpg")
    # image_path = "images/6.jpg"
    # image_name = image_path[find_last(image_path, '/') + 1:]
    # print image_name
    pass