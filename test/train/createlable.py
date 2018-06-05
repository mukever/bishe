import os
import random

img_path = "/root/samples/"

train_path = "./samples/"
train_val = open("train_val.txt","w+")

test_val = open("test_val.txt","w+")

map_txt = open("label-map.txt","r")

files = os.listdir(img_path)
print(files)
random.shuffle(files)
split_nums = int(len(files)*0.8)
train_files = files[:split_nums]
test_files = files[split_nums:]
# print(train_files)
# print(test_files)

train_label = []
test_label = []
map_label = [text.split("\n")[0] for text in map_txt.readlines() ]
print(map_label)
split_char = '_'
split_index = 0
for i in range(len(train_files)):
    label_text = str.upper(train_files[i].split(split_char)[split_index])

    while label_text.__len__()<10:
        label_text+="-"
    label_text = list(label_text)
    label_tmp =[]
    for i in range(len(label_text)):
        label_tmp.append(map_label.index(label_text[i]))

    label_tmp  = " ".join(str(i) for i in label_tmp)
    train_label.append(label_tmp)

for i in range(len(test_files)):
    label_text = str.upper(test_files[i].split(split_char)[split_index])


    while label_text.__len__()<10:
        label_text+="-"
    label_text = list(label_text)
    label_tmp = []
    for i in range(len(label_text)):
        label_tmp.append(map_label.index(label_text[i]))
    label_tmp  = " ".join(str(i) for i in label_tmp)
    test_label.append(label_tmp)

print(train_label)
print(test_label)

for i in range(train_files.__len__()):
    savestr = img_path+train_files[i]+" "+train_label[i]+"\n"
    print(savestr)
    train_val.write(savestr)
for i in range(test_files.__len__()):
    savestr = img_path+test_files[i] + " " + test_label[i]+"\n"
    print(savestr)
    test_val.write(savestr)

train_val.close()
test_val.close()