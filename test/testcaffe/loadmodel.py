#coding=utf-8

# import sys
# sys.path.append("/Users/diamond/envs/CTPN8/caffe/python")
# sys.path.append("/Users/diamond/envs/CTPN8/caffe/python/caffe")
import caffe
import numpy as np

from api.vocab import Vocab
from bishe.settings import MEDIA_CAFFE_PATH, MEDIA_CAFFE_PROTOTXT_PATH, MEDIA_CAFFE_LABEL_PATH

import matplotlib.pyplot as plt
# 编写一个函数，用于显示各层的参数
def show_feature(data, padsize=1, padval=0):
    data -= data.min();
    data /= data.max();

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])));
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3);
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval));

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)));
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:]);
    plt.imshow(data);
    plt.axis('off');
deploy=MEDIA_CAFFE_PROTOTXT_PATH   #deploy文件
# deploy='./resnet18.prototxt'    #deploy文件
# caffe_model=root + 'caffe.caffemodel'   #训练好的 caffemodel
caffe_model=MEDIA_CAFFE_PATH  #训练好的 caffemodel

labels_filename =MEDIA_CAFFE_LABEL_PATH  #类别名称文件，将数字标签转换回类别名称
img='./0.png'    #随机找的一张待测图片
net = caffe.Net(deploy,caffe_model,caffe.TEST)   #加载model和network
print(net.blobs['data'].data.shape)

#图片预处理设置
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})  #设定图片的shape格式(1,3,28,28)
transformer.set_transpose('data', (2,0,1))    #改变维度的顺序，由原始图片(28,28,3)变为(3,28,28)
transformer.set_mean('data', np.array([104,117,123]))    #减去均值，前面训练模型时没有减均值，这儿就不用
transformer.set_raw_scale('data', 255)    # 缩放到【0，255】之间
transformer.set_channel_swap('data', (2,1,0))   #交换通道，将图片由RGB变为BGR

im=caffe.io.load_image(img)                   #加载图片
net.blobs['data'].data[...] = transformer.preprocess('data',im)      #执行上面设置的图片预处理操作，并将图片载入到blob中
print(net.blobs['data'].data[...])
#执行测试
out = net.forward()
# 显示每一层
for layer_name, blob in net.blobs.items():
    print (layer_name + '\t' + str(blob.data.shape))
labels = np.loadtxt(labels_filename, str, delimiter='\n')   #读取类别名称文件
vocab = Vocab()
# print(labels)
# print(vocab.vocab)
for i in range(1,5):

    # print('---------------------\n',net.blobs['fc1000'+str(i)].data)
    prob= net.blobs['fc1000'+str(i)].data[0].flatten() #取出最后一层（Softmax）属于某个类别的概率值，并打印
    # print (prob)
    order=prob.argsort()[-1]  #将概率值排序，取出最大值所在的序号
    # print(order)
    print ('the class is:',labels[order] )  #将该序号转换成对应的类别名称，并打印

# 第一个卷积层，参数规模为(32,3,5,5)，即32个5*5的3通道filter
weight = net.params["conv1"][0].data
print(weight.shape)
show_feature(weight.transpose(0, 2, 3, 1))

# # 第二个卷积层的权值参数，共有32*32个filter,每个filter大小为5*5
# weight = net.params["conv2"][0].data;
# print(weight.shape)
# show_feature(weight.reshape(32 ** 2, 5, 5));
#
# # 第三个卷积层的权值，共有64*32个filter,每个filter大小为5*5，取其前1024个进行可视化
# weight = net.params["conv3"][0].data;
# print(weight.shape)
# show_feature(weight.reshape(64 * 32, 5, 5)[:1024]);