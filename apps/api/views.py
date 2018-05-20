import json
import threading
import time
import traceback

from django.conf.urls import url
from django.db.models import Sum, Count
from django.shortcuts import render
from datetime import datetime
# Create your views here.


#predict
import os
from django.http import HttpResponse, response, HttpResponseRedirect, request
import requests
from PIL import Image
from django.views.generic.base import View
from keras.models import model_from_json

from bishe.settings import MODEL_CAP_ROOT, MEDIA_CAP_ROOT, MEDIA_CAP_DB_PATH, MEDIA_URL, BASE_DIR
from spider_monitor.models import SpiderInfo, PredisctList
from spider_monitor.plugins import CJsonEncoder
from yzm_info.models import YzmInfo
from .vocab import *



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
                if spider_id == '4':
                    # print(spider.name)
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
            self.posturl = 'https://ln.122.gov.cn/m/publicquery/scores/?jszh=sadasd&dabh=123456789012&captcha=%s'
            self.header = {
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',

                'Referer':'https://ln.122.gov.cn/views/inquiry.html',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',

               }

            # self.data = {
            #
            # }

            ####load model
            print('loadmodel::', self.spider.update_model.path)
            print('loadcnn:::', self.spider.update_net.path)
            self.model = model_from_json(open(self.spider.update_net.path).read())
            self.model.load_weights(self.spider.update_model.path)
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

            for i in range(20):
                img = _session.get(self.spider.url.image_url)
                temp_img = img.content

                ######save pic
                temp_name = str(datetime.now())+ ".jpg"

                fp = open(folder_path + temp_name , "wb")
                fp.write(temp_img)
                fp.close()

                #####read img
                image = Image.open(folder_path + temp_name)

                ### detail
                wide, high = image.size
                for j in range(wide):
                    image.putpixel((j, 0), (255, 255, 255))
                for j in range(high):
                    image.putpixel((0, j), (255, 255, 255))
                X_ = np.empty((1, 32, 90, 3), dtype='float32')

                ### predict
                X_[0] = np.array(image) / 255
                Y_pred = self.model.predict(X_, 1, 1)
                Pred_text = Vocab().one_hot_to_text(Y_pred[0])
                print(Pred_text)
                temp_url = self.posturl % (Pred_text)
                reconvene = _session.post(temp_url ,headers= self.header)
                code = json.loads(reconvene.content.decode('utf8'))['code']
                print(reconvene.content.decode('utf8'))
                ####('1', '正确'), ('0', '错误')
                pre_st = 0
                # print(type(code))
                if code ==404:
                    pre_st = 1
                else:
                    pass

                db_path = MEDIA_CAP_DB_PATH+medile_path+temp_name

                predict_model = PredisctList()

                predict_model.spidername = self.spider
                predict_model.yzmname = self.spider.url
                predict_model.status = pre_st
                predict_model.img = db_path
                predict_model.predict = Pred_text
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


class GetYzmInfoView(View):

    def get(self,request,yzm_id):
        yzminfo = YzmInfo.objects.filter(id=yzm_id).first()
        js = yzminfo.toJSON()
        print(js)
        return HttpResponse(json.dumps(js), content_type='application/json')

