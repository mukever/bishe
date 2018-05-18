# -*- coding:utf-8 -*-

import cv2
import numpy as np
import os

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




    #打印处理结果
    def printcv2(self):
        cv2.namedWindow("Image")
        cv2.imshow("Image", self.img_src_cv2)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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


    def runLiaoning(self):
        # # self.addImage()
        # self.printcv2()
        # # thresh = icl.otsu(img_src_cv2)
        self.binaryzation( power=1.0)
        # self.printcv2()
        return self.img_src_cv2

if __name__ == '__main__':

    #img path
    img_path = "2K95.jpg"
    #read img
    cv2_img = cv2.imread("")
    clean = Clean(cv2_img)
    cv2_img = clean.addImage()
    cv2_img = clean.binaryzation()
    clean.printcv2()
