import json
import os,django
import shutil
import time
from datetime import datetime

from bishe.settings import MEDIA_CAP_ROOT, MEDIA_CAFFE_PROTOTXT_PATH, MEDIA_CAFFE_PATH, MEDIA_CAFFE_LABEL_PATH

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bishe.settings")# project_name 项目名称
django.setup()
import requests
def getTime():
    # 获得当前系统时间的字符串
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('localtime=' + localtime)
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    return year,month
preurl  ='http://zhixing.court.gov.cn/search/'
url = 'http://zhixing.court.gov.cn/search/newsearch'
imgurl = 'http://zhixing.court.gov.cn/search/captcha.do?captchaId=9c9240cac2194896be0ec82ce2abc662&random=0.7856124985578259'

data={
'searchCourtName': '全国法院（包含地方各级法院) ',
'selectCourtId': '1',
'selectCourtArrange': '1',
'pname': 'as',
'cardNum': '123456789123456',
'j_captcha': "",
'captchaId':'9c9240cac2194896be0ec82ce2abc662',
}

#### create folder
year, month = getTime()
medile_path = '交管信息/'+str(year)+'/'+str(month)+'/'
###path
folder_path = MEDIA_CAP_ROOT+medile_path
folder = os.path.exists(folder_path)
print(folder)
if not folder:
    os.makedirs(folder_path)

sess = requests.session()
print(sess.get(preurl).content.decode('utf8'))
k = sess.get(imgurl)
print(k.content)
temp_img = k.content

######save pic
temp_name = str(datetime.now())+ ".jpg"

fp = open(folder_path + temp_name , "wb")
fp.write(temp_img)
fp.close()
print(folder_path+temp_name)
#####read img
import caffe
import numpy as np
deploy = MEDIA_CAFFE_PROTOTXT_PATH  # deploy文件
caffe_model = MEDIA_CAFFE_PATH  # 训练好的 caffemodel
labels_filename = MEDIA_CAFFE_LABEL_PATH  # 类别名称文件，将数字标签转换回类别名称
LABELS = np.loadtxt(labels_filename, str, delimiter='\n')   #读取类别名称文件
CAFFENET = caffe.Net(deploy, caffe_model, caffe.TEST)  # 加载model和network

# 图片预处理设置
Transformer = caffe.io.Transformer({'data': CAFFENET.blobs['data'].data.shape})  # 设定图片的shape格式(1,3,28,28)
Transformer.set_transpose('data', (2, 0, 1))  # 改变维度的顺序，由原始图片(28,28,3)变为(3,28,28)
Transformer.set_mean('data', np.array([104, 117, 123]))  # 减去均值，前面训练模型时没有减均值，这儿就不用
Transformer.set_raw_scale('data', 255)  # 缩放到【0，255】之间
Transformer.set_channel_swap('data', (2, 1, 0))  # 交换通道，将图片由RGB变为BGR


im = caffe.io.load_image(folder_path + temp_name)  # 加载图片
### detail
CAFFENET.blobs['data'].data[...] = Transformer.preprocess('data', im)  # 执行上面设置的图片预处理操作，并将图片载入到blob中
### predict
CAFFENET.forward()
Predisct = ""
pre_st = 0
for i in range(1, 5):
    # print('---------------------\n',net.blobs['fc1000'+str(i)].data)
    prob = CAFFENET.blobs['fc1000' + str(i)].data[0].flatten()  # 取出最后一层（Softmax）属于某个类别的概率值，并打印
    # print (prob)
    order = prob.argsort()[-1]  # 将概率值排序，取出最大值所在的序号
    # print(order)
    Predisct+=LABELS[order]  # 将该序号转换成对应的类别名称，并打印
print(Predisct)
data['j_captcha'] = Predisct
print(data)
rs = sess.post(url,data)
print(rs.content.decode('utf8'))