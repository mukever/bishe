import os
import random
import sys
import numpy as np
import lmdb

import caffe

# 根据多标签的位置选择从数据库、文件等中读取每幅图片的多标签，将其构造成一维的np.array类型，并追加入all_labels列表

# Add your code of reading labels here ！
img_path = "/root/samples/"

map_txt = open("label-map.txt","r")

files = os.listdir(img_path)
# print(files)
# random.shuffle(files)
# split_nums = int(len(files)*0.8)
train_files = files[:100]
test_files = files[:100]
print(train_files.__len__())
# print(test_files)

map_label = [text.split("\n")[0] for text in map_txt.readlines() ]
print(map_label)
split_char = '_'
split_index = 0
all_labels = []
for i in range(len(train_files)):
    label_text = str.upper(train_files[i].split(split_char)[split_index])

    while label_text.__len__()<10:
        label_text+="-"
    label_text = list(label_text)
    label_tmp =[]
    for i in range(len(label_text)):
        label_tmp.append(map_label.index(label_text[i]))

    all_labels.append(label_tmp)


all_labels = np.array(all_labels)
print(all_labels)
# 创建标签LMDB
key = 0
lmdb_path = "./train_label_lmdb"
env = lmdb.open(lmdb_path, map_size=int(1e12))
with env.begin(write=True) as txn:
    for labels in all_labels:
        datum = caffe.proto.caffe_pb2.Datum()
        print(labels.shape[0])
        datum.channels = 10
        datum.height = 1
        datum.width =  1
        datum.data = labels.tostring()          # or .tobytes() if numpy < 1.9
        datum.label = 0
        key_str = '{:08}'.format(key)

        txn.put(key_str.encode('ascii'), datum.SerializeToString())
        key += 1

