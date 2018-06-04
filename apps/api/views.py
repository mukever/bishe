import json
import threading
import time
import traceback
import numpy as np
from PIL import Image

from django.conf.urls import url
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Sum, Count
from django.shortcuts import render
from datetime import datetime
# Create your views here.


#predict
import os
from django.http import HttpResponse, HttpResponseRedirect
import requests
from PIL import Image
from django.views.generic.base import View
import caffe
from imageio import save

from .postutils import  chaojicheck
from bishe.settings import MODEL_CAP_ROOT, MEDIA_CAP_ROOT, MEDIA_CAP_DB_PATH, MEDIA_URL, BASE_DIR,  \
    MEDIA_API_PATH
from monitor.models import SpiderInfo, PredisctList
from monitor.plugins import CJsonEncoder
from .vocab import *
from bishe.settings import MEDIA_CAFFE_PATH, MEDIA_CAFFE_PROTOTXT_PATH, MEDIA_CAFFE_LABEL_PATH

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


class SpiderControView(View):

    def get(self,request,spider_id):
        print(spider_id)

        res = dict
        if not request.user.is_authenticated():

            res['errorcode'] = '100'
            res['message'] = '用户未登录'
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            spider = SpiderInfo.objects.filter(id=spider_id).first()
            if spider is None:
                res['errorcode'] = '101'
                res['message'] = '该爬虫信息不存在'
                return HttpResponse(json.dumps(res), content_type='application/json')
            else:
                print(spider.name)
                if spider.status == '2':
                    ####start run
                    spider_thread = SpiderThread(spider)
                    # session = request.session
                    # session[spider.name] = spider_thread
                    spider_thread.start()
                    #### save
                    spider.status = '1'
                    spider.run_nums += 1
                elif spider.status =='1':
                    ###stop
                    pass
                    ### save
                    spider.status = '2'
                spider.save()

                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # print(json.dumps(res))

class SpiderThread(threading.Thread):
    def __init__(self, spider):
        try:
            super(SpiderThread, self).__init__()
            self.spider = spider

        except Exception as e:
            traceback.print_exc()
        finally:
            ### finsish task
            self.spider.status = '2'
            self.spider.save()

    def run(self):
        try:

            #### create folder
            year, month = getTime()
            medile_path = self.spider.url.name+'/'+str(year)+'/'+str(month)+'/'
            ###path
            folder_path = MEDIA_CAP_ROOT+medile_path
            folder = os.path.exists(folder_path)
            print(folder)
            if not folder:
                os.makedirs(folder_path)

            ######download pic
            _session = requests.session()

            ecpohs = 10
            if self.spider.needcheck == '1':
                ecpohs=30

            for i in range(ecpohs):
                img = _session.get(self.spider.url.image_url)
                temp_img = img.content

                ######save pic
                temp_name = str(datetime.now())+ ".jpg"

                fp = open(folder_path + temp_name , "wb")
                fp.write(temp_img)
                fp.close()
                print(folder_path+temp_name)
                #####read img
                im = caffe.io.load_image(folder_path + temp_name)  # 加载图片
                ### detail
                CAFFENET.blobs['data'].data[...] = Transformer.preprocess('data', im)  # 执行上面设置的图片预处理操作，并将图片载入到blob中
                ### predict
                CAFFENET.forward()
                Predisct = ""
                pre_st = 0
                for i in range(1, int(self.spider.url.tag)+1):
                    # print('---------------------\n',net.blobs['fc1000'+str(i)].data)
                    prob = CAFFENET.blobs['fc1000' + str(i)].data[0].flatten()  # 取出最后一层（Softmax）属于某个类别的概率值，并打印
                    # print (prob)
                    order = prob.argsort()[-1]  # 将概率值排序，取出最大值所在的序号
                    # print(order)
                    Predisct+=LABELS[order]  # 将该序号转换成对应的类别名称，并打印
                print(Predisct)
                if self.spider.needcheck=='2':
                    pre_st = chaojicheck(folder_path+temp_name,Predisct,self.spider.url.tag)

                db_path = MEDIA_CAP_DB_PATH+medile_path+temp_name

                predict_model = PredisctList()

                predict_model.spidername = self.spider
                predict_model.yzmname = self.spider.url
                predict_model.status = pre_st
                predict_model.img = db_path
                predict_model.predict = Predisct
                temp_time = datetime.now()
                print(temp_time)
                predict_model.add_time = temp_time
                predict_model.save()
                self.spider.predict_nums+=1
                self.spider.save()
        except Exception as e:
            ### finsish task
            traceback.print_exc()
        finally:
            self.spider.status = '2'
            self.spider.save()



##### 返回图表数据

class PrediacListDataView(View):

    def get(self,request):

        if not request.user.is_authenticated():
            data = getPreDiactData()
            data_json = json.dumps(data,cls=CJsonEncoder)
            print(data_json)
            return HttpResponse(data_json)
        else:
            data = getPreDiactData()
            data_json = json.dumps(data, cls=CJsonEncoder)
            print(data_json)
            return HttpResponse(data_json)

class PredictAPI(View):

    def get(self,request):

        data = {'code':'1234'}
        data_json = json.dumps(data)
        print(data_json)
        return HttpResponse(data_json)
    def post(self,request):


        img = request.FILES.get('pic')
        tag  = request.POST.get('tag')
        destination = open(MEDIA_API_PATH, 'wb+')  # 打开特定的文件进行二进制的写操作
        destination.write(img.read())
        destination.close()

        ###caffe
        im = caffe.io.load_image(MEDIA_API_PATH)  # 加载图片
        ### detail
        CAFFENET.blobs['data'].data[...] = Transformer.preprocess('data', im)  # 执行上面设置的图片预处理操作，并将图片载入到blob中
        ### predict
        CAFFENET.forward()
        Predisct = ""
        pre_st = 0
        for i in range(1, int(tag) + 1):
            # print('---------------------\n',net.blobs['fc1000'+str(i)].data)
            prob = CAFFENET.blobs['fc1000' + str(i)].data[0].flatten()  # 取出最后一层（Softmax）属于某个类别的概率值，并打印
            # print (prob)
            order = prob.argsort()[-1]  # 将概率值排序，取出最大值所在的序号
            # print(order)
            Predisct += LABELS[order]  # 将该序号转换成对应的类别名称，并打印
        print(Predisct)

        data = {'code': Predisct}
        data_json = json.dumps(data)
        print(data_json)
        return HttpResponse(data_json)

def getPreDiactData():
    select = {'minute': "CAST(DATE_FORMAT(add_time, '%%Y-%%m-%%d %%H-%%i--01') AS DATETIME)"}
    # print(select)

    Echart_data = dict()

    spiderids = SpiderInfo.objects.values('id', 'name')

    all_data = []

    for spiderid in spiderids:

        ### 构造Echarts数据集
        data = dict()
        spider_id = spiderid['id']
        results = PredisctList.objects.filter(spidername=spider_id).extra(select=select).values('minute').annotate(
            sum=Sum('status')).order_by('minute')
        results_count = PredisctList.objects.filter(spidername=spider_id).extra(select=select).values(
            'minute').annotate(
            sum=Count('status')).order_by('minute')

        # print('size',results.__len__())
        # print(spiderid['name'])
        data_acc_list = []
        data_date_list = []

        #####封装数据
        if results.__len__() == 0:
            continue
        for i in range(len(results)):
            if results_count[i]['sum'] == 0:
                data_acc_list.append(0.0)
                # continue
            else:
                data_acc_list.append(results[i]['sum'] * 1.0 / results_count[i]['sum'] * 100)
                data_date_list.append(results[i]['minute'])

        data['data_sum'] = data_acc_list
        data['data_date'] = data_date_list
        data['data_num'] = data_acc_list.__len__()
        data['data_name'] = spiderid['name']
        all_data.append(data)
    Echart_data['data'] = all_data
    Echart_data['count'] = all_data.__len__()


    return Echart_data


def getTime():
    # 获得当前系统时间的字符串
    localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('localtime=' + localtime)
    # 系统当前时间年份
    year = time.strftime('%Y', time.localtime(time.time()))
    # 月份
    month = time.strftime('%m', time.localtime(time.time()))
    return year,month





