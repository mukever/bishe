# -*- coding:utf-8 -*-


from .Model import *
from .Clean import *

import cv2
import os
import numpy as np
import sys
import time
import urllib


class Beijing():

    def __init__(self):
        self.number = 4
        self.data = []
        self.label = []

        # 预处理
    def pretreatment(self, train_data_root):
        if os.path.isdir(train_data_root):
            for picname in os.listdir(train_data_root):
                print (picname)
                dataof4, labelof4 = self.dofile(train_data_root, picname)
                data_ = list(dataof4)
                for i in range(len(data_)):
                    self.data.append(data_[i])
                    self.label.append(labelof4[i])
        else:
            dataof4, labelof4 = self.dofile(train_data_root)
            data_ = list(dataof4)
            for i in range(len(data_)):
                self.data.append(data_[i])
                if len(labelof4)!=0:
                    self.label.append(labelof4[i])

    def predict(self,src_path):
        time1 = time.time()
        data = []
        label = []
        dataof4, labelof4 = self.dofile(src_path)
        data_ = list(dataof4)
        for i in range(len(data_)):
            data.append(data_[i])
            if len(labelof4) != 0:
                label.append(labelof4[i])
        print ("图片复原+处理总时间:",time.time()-time1)
        return data,label



    # 单张图片
    def dofile(self,root,picname = ""):

        dataof4 = []
        labelof4 = []
        # cv2读取pic
        # cv2_data = cv2.imread(root + picname)
        print ("url:",root)
        resp = requests.get(root)
        image = np.asarray(bytearray(resp.content), dtype="uint8")
        cv2_data = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # win = cv2.namedWindow('test win', flags=0)
        #
        # cv2.imshow('test win', cv2_data)
        # cv2.waitKey(0)

        # cv2.imwrite("/home/mukever/1.png", cv2_data)
        print ("北京图片已保存")
        print ("北京---url地址读取成功")
        # time1 = time.time()
        # f = Fuyuan(cv2_data)
        # cv2_data = f.run()
        # print "图片复原时间:",time.time()-time1 ," ",
        time1 = time.time()
        cv2_data = Clean(cv2_data).runBeijing()
        # print "图片去噪处理:", time.time() - time1
        # 裁掉边框
        # win = cv2.namedWindow('test win', flags=0)
        #
        # cv2.imshow('test win', cv2_data)
        # cv2.waitKey(0)

        im1 = cv2_data[10:47, 30:60, ]
        im2 = cv2_data[10:47, 60:90, ]
        im3 = cv2_data[10:47, 90:120, ]
        im4 = cv2_data[10:47, 120:150, ]

        im_list = [im1, im2, im3, im4]
        # t = ImageClean()
        for k in range(self.number):
            im_i = im_list[k]
            h = im_i.shape[0]
            w = im_i.shape[1]
            # t.printcv2(im_i)
            tmp_data = [0 for i in range(h * w)]
            for i in range(h):
                for j in range(w):
                    # print im_i
                    if im_i[i, j] == 0:

                        tmp_data[i * j + j] = 1

            dataof4.append(tmp_data)
            if picname !="":
                labelof4.append(picname[k])
        return dataof4, labelof4


    def svaeData(self, name):
        data = np.array(self.data)
        label = np.array(self.label)
        np.savez(name, Data=data, Label=label)

if __name__ == '__main__':
    train_root ="/home/mukever/PycharmProjects/yanzhengma/com/beijin/train/"
    test_root = "/home/mukever/PycharmProjects/yanzhengma/com/beijin/test/"
    # b = Beijing()
    # b.dofile()
    print ("Train---------------------------------------------------")
    b = Beijing()
    b.pretreatment(train_root)
    name = "beijing"
    b.svaeData(name)
    res = np.load(name+".npz")
    # 进行分类
    print ("Test---------------------------------------------------")
    b_c = Beijing()
    b_c.pretreatment(test_root)
    test_x = np.array(b_c.data)
    test_y = np.array(b_c.label)
    train_x = res['Data']
    train_y = res['Label']
    print (train_x,train_y)
    print ("测试集样本数：",len(test_x)/4)
    m = Model()
    m.getmodel(train_x, train_y, "",test_x,test_y)