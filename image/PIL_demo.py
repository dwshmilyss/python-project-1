#!/usr/bin/env python
# encoding: utf-8


"""
@version: v1.0
@author: duanwei
@license: Apache Licence 
@contact: 4064865@qq.com
@site: http://blog.csdn.net/dwshmilyss
@software: PyCharm
@file: PIL_demo.py
@time: 2018/1/8 11:31
"""
import sys
from PIL import Image
import argparse
default_encoding = "utf-8"
if (default_encoding != sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)


def func():
    pass


class Main():
    def __init__(self):
        pass


parser = argparse.ArgumentParser('')

parser.add_argument('file') #input file
parser.add_argument('-o', '--output')  #output file
parser.add_argument('--width', type = int, default = 80) #output character width
parser.add_argument('-height', type = int, default = 80) #output character height

#get parameters
args = parser.parse_args()

IMG = args.file
OUTPUT = args.output
WIDTH = args.width
HEIGHT = args.height



ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

def get_char(r, b, g, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


if __name__ == "__main__":
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    print txt

    #output the result into a file
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)

    else:
        with open("output.txt", 'w') as f:
            f.write(txt)
    pass