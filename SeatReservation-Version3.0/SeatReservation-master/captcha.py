# coding=utf-8

# Created by Deserts
# email: i@panjunwen.com
# site: https://panjunwen.com/
# date: 2016-08-20

from PIL import Image
from io import StringIO
import math
import os


class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        # relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1


table1 = []
threshold1 = 130
for i in range(256):
    if i < threshold1:
        table1.append(0)
    else:
        table1.append(1)


def blur1(im):
    '''
    :param im:
    :return: im
    PIL.im
    convert the original im Pillow object
    '''
    # translating a color image to black and white (mode "L")
    im = im.convert('L')
    # Maps this image through a lookup table or function
    im = im.point(table1, '1')
    return im

def captcha(img):
    # 获取json.string格式的图片，并转换成PNG
    im = Image.open(StringIO(img))
    # 测试用
    # 我也不知道为什么换一个文件就出问题了
    im.save("captcha.png", "PNG")
    im2 = blur1(im)
    im2 = im2.convert("P")
    v = VectorCompare()
    # 没有9,o,z?
    iconset = '012345678abcdefghijklmnpqrstuvwxy'
    imageset = []

    for letter in iconset:
        for img in os.listdir('./iconset/%s/' % (letter)):
            temp = []
            if img != "Thumbs.db" and img != ".DS_Store":
                temp.append(buildvector(Image.open("./iconset/%s/%s" % (letter, img))))
            imageset.append({letter: temp})

    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = []
    for y in range(im2.size[0]):
        for x in range(im2.size[1]):
            pix = im2.getpixel((y, x))
            if pix != 255:
                inletter = True
        if foundletter is False and inletter is True:
            foundletter = True
            start = y
        if foundletter is True and inletter is False:
            foundletter = False
            end = y
            letters.append((start, end))
        inletter = False

    count = 0
    res = str()
    for letter in letters:
        # m = hashlib.md5()
        im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))
        guess = []
        for image in imageset:
            for x, y in image.items():
                if len(y) != 0:
                    guess.append((v.relation(y[0], buildvector(im3)), x))
        guess.sort(reverse=True)
        res += str(guess[0][1])
        count += 1
    return str(res)
