import random

import caffe
import lmdb
import os

from bishe.settings import MEDIA_CAFFE_PATH, MEDIA_CAFFE_PROTOTXT_PATH, MEDIA_CAFFE_LABEL_PATH
import numpy as np
# deploy = MEDIA_CAFFE_PROTOTXT_PATH  # deploy文件
# caffe_model = MEDIA_CAFFE_PATH  # 训练好的 caffemodel
# labels_filename = MEDIA_CAFFE_LABEL_PATH  # 类别名称文件，将数字标签转换回类别名称
# LABELS = np.loadtxt(labels_filename, str, delimiter='\n')   #读取类别名称文件
# CAFFENET = caffe.Net(deploy, caffe_model, caffe.TEST)  # 加载model和network
# print(CAFFENET.blobs['data'].data.shape)
# 图片预处理设置
Transformer = caffe.io.Transformer({'data': (1, 3, 224, 224)})  # 设定图片的shape格式(1,3,28,28)
Transformer.set_transpose('data', (2, 0, 1))  # 改变维度的顺序，由原始图片(28,28,3)变为(3,28,28)
Transformer.set_mean('data', np.array([104, 117, 123]))  # 减去均值，前面训练模型时没有减均值，这儿就不用
Transformer.set_raw_scale('data', 255)  # 缩放到【0，255】之间
Transformer.set_channel_swap('data', (2, 1, 0))  # 交换通道，将图片由RGB变为BGR
img_path = "/root/samples/"

map_txt = open("label-map.txt","r")
map_label = [text.split("\n")[0] for text in map_txt.readlines() ]
files = os.listdir(img_path)
print(files.__len__())
train_files = files[0:100]
split_char = '_'
split_index = 0
all_labels = []
all_images = []
for i in range(len(train_files)):
    im = caffe.io.load_image(img_path+train_files[i]) # 加载图片
    ### detail
    data=Transformer.preprocess('data', im)  # 执行上面设置的图片预处理操作，并将图片载入到blob中
    all_images.append(data)
all_images = np.array(all_images)
# all_labels =np.array(all_labels)
key = 0
lmdb_path = "./train_data_lmdb"
env = lmdb.open(lmdb_path, map_size=int(1e12))
with env.begin(write=True) as txn:
    for i in range(len(all_labels)):
        print(all_images[i].shape)
        print("已处理"+str(i)+"张图片")
        datum = caffe.proto.caffe_pb2.Datum()
        datum.channels = 3
        datum.height = 224
        datum.width =  224
        datum.data = all_images[i].tobytes()     # or .tobytes() if numpy < 1.9
        # datum.label = " ".join(str(j) for j in all_labels[i])
        datum.label = 0
        key_str = '{:08}'.format(key)

        txn.put(key_str.encode('ascii'), datum.SerializeToString())
        key += 1
