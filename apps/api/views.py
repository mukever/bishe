import json
import string
import threading
import time
import traceback

import bs4
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
from numpy import unicode

from .postutils import  chaojicheck
from bishe.settings import MODEL_CAP_ROOT, MEDIA_CAP_ROOT, MEDIA_CAP_DB_PATH, MEDIA_URL, BASE_DIR, \
    MEDIA_API_PATH, TIMEOUT
from monitor.models import SpiderInfo, PredisctList, CheckInfo
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

header = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer':'https://ln.122.gov.cn/views/inquiry.html',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',

}
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

            ecpohs = self.spider.spider_run_nums
            # if self.spider.needcheck == '1':
            #     ecpohs=1

            for i in range(ecpohs):
                # proxy = {'http': '33.33.33.10:8118'}
                try:

                    proxy_ip_port = requests.get('http://123.207.35.36:5010/get/',timeout=TIMEOUT).content.decode('utf8')
                    proxy = {'http': proxy_ip_port}
                    print(proxy)

                    #判断proxy可用性
                    print(bs4.BeautifulSoup(requests.get('http://ip.chinaz.com/', proxies=proxy,timeout=TIMEOUT).content,
                                            'html5lib').find("p", {
                        "class": "getlist pl10"}).get_text())

                    img = _session.get(self.spider.url.image_url,proxies=proxy,timeout=TIMEOUT)
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
                    # print(Predisct)
                    msg = "无验证"
                    if self.spider.needcheck=='2':
                        pre_st,msg = checkyzm(self.spider,Predisct,_session,proxy)

                    #pre_st = checkyzm(self.spider, Predisct,_session)
                    print(Predisct)
                    db_path = MEDIA_CAP_DB_PATH+medile_path+temp_name

                    predict_model = PredisctList()

                    predict_model.spidername = self.spider
                    predict_model.yzmname = self.spider.url
                    predict_model.status = pre_st
                    predict_model.img = db_path
                    predict_model.desc = msg
                    predict_model.predict = Predisct
                    temp_time = datetime.now()
                    print(temp_time)
                    predict_model.add_time = temp_time
                    predict_model.save()
                    self.spider.predict_nums+=1
                    self.spider.save()
                except requests.exceptions.ReadTimeout as e:
                    print("代理异常  requests.exceptions.ReadTimeout")
                except requests.exceptions.ProxyError as e:
                    print("代理异常  requests.exceptions.ProxyError ")
                    # traceback.print_exc()
                except requests.exceptions.ConnectTimeout as e:
                    print("网络异常，代理超时 requests.exceptions.ConnectTimeout")
                    # traceback.print_exc()
                except requests.exceptions.ConnectionError as e:
                    print("网络异常,连接出错 requests.exceptions.ConnectionError")
                    # traceback.print_exc()
                except AttributeError as e:
                    print("确认代理信息失败AttributeError")
                except Exception as e:
                    traceback.print_exc()
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
            data_json = json.dumps(data,cls=CJsonEncoder,ensure_ascii=False)
            print(data_json)
            return HttpResponse(data_json)
        else:
            data = getPreDiactData()
            data_json = json.dumps(data, cls=CJsonEncoder,ensure_ascii=False)
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





def checkyzm(spider,predictvalue,re_sssion,proxy):

    status = 0
    msg ="验证通过"
    try:

        #获取提交数据信息
        print("ready check")
        print(spider)
        all_attrs = CheckInfo.objects.filter(name=spider).all()
        # 获取提交数据地址
        dicts = {}
        cap = ""
        for attrs in all_attrs:

            if attrs.desc=="验证码":
                cap = attrs.attr
            if attrs.desc =="随机产生":
                attrs.value = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            dicts[attrs.attr] = attrs.value

        dicts[cap] = predictvalue
        print(dicts)
        post_url = spider.posturl
        #封装爬虫信息

        if spider.check == '3':
            res = re_sssion.post(post_url,data=dicts,headers=header,proxies=proxy,timeout=TIMEOUT).content.decode('utf8')

            if "验证码" in res:
                status = 0
                print("验证码错误")
                print(res)
            else:
                status = 1
                print("验证码正确")
        elif spider.check=='2':
            post_url+='?'
            li = list(dicts.keys())
            for i in  range(li.__len__()):
                if i==0:
                    post_url+=(li[i]+"="+dicts[li[i]])
                else:
                    post_url += ("&"+li[i] + "=" + dicts[li[i]])
            # print(post_url)
            # 提交数据
            res = re_sssion.get(post_url, headers=header,proxies=proxy,timeout=TIMEOUT)
            bianma = spider.get_bianma_display()
            print(bianma)
            text = res.content.decode(bianma)
            print("数据提交完毕")
            print(text)
            if "验证码" in text:
                status = 0
                print("验证码错误")
            else:
                #获取结果
                status = 1
                print("验证码正确")


    except requests.exceptions.ReadTimeout as e:

        print("代理异常  requests.exceptions.ReadTimeout")
        msg='代理异常  requests.exceptions.ReadTimeout'
        status = 0
    except requests.exceptions.ProxyError as e:

        print("代理异常  requests.exceptions.ProxyError ")
        msg = '代理异常 requests.exceptions.ProxyError '

        status = 0
        # traceback.print_exc()

    except requests.exceptions.ConnectTimeout as e:

        print("网络异常，代理超时 requests.exceptions.ConnectTimeout")
        msg = '网络异常，代理超时 requests.exceptions.ConnectTimeout'
        # traceback.print_exc()

    except requests.exceptions.ConnectionError as e:

        print("网络异常,连接出错 requests.exceptions.ConnectionError")
        msg = '网络异常,连接出错 requests.exceptions.ConnectionError'
        status = 0
        # traceback.print_exc()

    except AttributeError as e:

        print("确认代理信息失败AttributeError")
        msg = '确认代理信息失败AttributeError'
        status = 0
    except Exception as e:
        msg = '系统错误'
        status = 0
        traceback.print_exc()
    finally:
        return status,msg
