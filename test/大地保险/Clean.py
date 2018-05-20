# -*- coding:utf-8 -*-

import urllib

import cv2
import numpy as np
import os

import requests
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from numpy.linalg import linalg
from numpy.random import random
from scipy.ndimage import filters


class Clean():


    def __init__(self,img_src_cv2):
        self.img_src_cv2 = img_src_cv2
    # 增亮
    def addImage(self):

        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
                # 图像加亮
                r = self.img_src_cv2[i, j, 0] * 1.1 + 30
                g = self.img_src_cv2[i, j, 1] * 1.1 + 30
                b = self.img_src_cv2[i, j, 2] * 1.1 + 30
                # print(r ,g ,b)
                if r >= 255:
                    self.img_src_cv2[i, j, 0] = 255
                if g >= 255:
                    self.img_src_cv2[i, j, 1] = 255
                if b>= 255:
                    self.img_src_cv2[i, j, 2] = 255

    # 获取阈值
    def otsu(self):
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        histData = [0 for i in range(256)]

        for i in range(h):
            for j in range(w):
                # print add_img[i,j,0]
                histData[self.img_src_cv2[i,j,0]] += 1
        sum = 0

        for t in range(len(histData)):
            sum += t*histData[t]

        total = w * h
        sumB = 0;
        wB = 0;
        wF = 0;
        varMax = 0;
        threshold = 0;

        for t in range(256):
            wB += histData[t]
            # print wB
            if wB == 0:
                continue
            wF = total - wB
            if wF == 0:
                break
            sumB += (float)(t * histData[t])
            mB = sumB / wB
            mF = (sum - sumB) / wF
            varBetween = wB * wF * (mB - mF) * (mB - mF)
            if varBetween > varMax:
                varMax = varBetween
                threshold = t
        return threshold

    def deleteblack(self,th):
        if th <= 40 :
            # print "无法去除噪点"
            return
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
               if self.img_src_cv2[i,j][0] <30 and self.img_src_cv2[i,j][1]<30 and self.img_src_cv2[i,j][2] <30:
                    self.img_src_cv2[i,j] = 255

    #二值化
    def binaryzation(self,threshold = -1,power = 1.0):
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        if threshold == -1:
            threshold = self.otsu()
        self.img_src_cv2 = cv2.cvtColor(self.img_src_cv2, cv2.COLOR_RGB2GRAY)
        for i in range(h):
            for j in range(w):
                if self.img_src_cv2[i,j] >= threshold/power:
                    self.img_src_cv2[i,j] = 255
                else:
                    self.img_src_cv2[i,j] = 0

    # 干扰线降噪
    def interference_line(self):

        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        # ！！！opencv矩阵点是反的
        # img[1,2] 1:图片的高度，2：图片的宽度
        for y in range(1, w - 1):
            for x in range(1, h - 1):
                count = 0
                if any(self.img_src_cv2[x, y - 1]) > 245:
                    count = count + 1
                if any(self.img_src_cv2[x, y + 1]) > 245:
                    count = count + 1
                if any(self.img_src_cv2[x - 1, y]) > 245:
                    count = count + 1
                if any(self.img_src_cv2[x + 1, y]) > 245:
                    count = count + 1
                if count > 2:
                    self.img_src_cv2[x, y] = 255

    #根据字符颜色去除噪点
    def deletepointByRGB(self):
        R = [0 for i in range(0, 256)]
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
               if(self.img_src_cv2[i][j] > (200,200,200)):
                   pass
                   # R[]

    # 根据字符R颜色去除噪点
    def deletepointByR(self):
        R = [0 for i in range(0,256)]
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
                # print(self.img_src_cv2[i][j][0])
                R[self.img_src_cv2[i][j][0]]+=1
        return R

    # 根据字符G颜色去除噪点
    def deletepointByG(self):
        R = [0 for i in range(0, 256)]
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
                # print(self.img_src_cv2[i][j][0])
                R[self.img_src_cv2[i][j][1]] += 1
        return R

    # 根据字符B颜色去除噪点
    def deletepointByB(self):
        R = [0 for i in range(0, 256)]
        h = self.img_src_cv2.shape[0]
        w = self.img_src_cv2.shape[1]
        for i in range(h):
            for j in range(w):
                # print(self.img_src_cv2[i][j][0])
                R[self.img_src_cv2[i][j][2]] += 1
        return R

    #打印处理结果
    def printcv2(self):
        cv2.namedWindow("Image")
        cv2.imshow("Image", self.img_src_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self):
        img = Image.fromarray(self.img_src_cv2)
        img.save("temp.jpg","jpeg")

    def runBeijing(self):
        # self.addImage()
        th = self.otsu()
        if th > 40:
            self.deleteblack(th)
        # self.printcv2()
        # thresh = icl.otsu(img_src_cv2)
        self.binaryzation( power=0.8)
        # self.printcv2()
        return self.img_src_cv2




        
if __name__ == '__main__':
    root = 'https://www.creditease.cn//servlet/validateCodeServlet?%27+new%20Date().getTime())'
    resp = requests.get(root)
    # print(resp.content)
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    cv2_data = cv2.imdecode(image, cv2.IMREAD_COLOR)

    clean = Clean(cv2_data)
    # clean.printcv2()
    clean.binaryzation()
    clean.save()






