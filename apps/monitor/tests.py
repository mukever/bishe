
import os,django

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bishe.settings")# project_name 项目名称
django.setup()

from django.db.models import Count, Sum
from django.test import TestCase
# Create your tests here.

from django.db import connection


from monitor.models import PredisctList, SpiderInfo
from monitor.plugins import *

if __name__ == '__main__':

    select = {'minute': "CAST(DATE_FORMAT(add_time, '%%Y-%%m-%%d %%H-%%i--01') AS DATETIME)"}
    # print(select)

    Echart_data = dict()

    spiderids = SpiderInfo.objects.values('id','name')

    all_data = []

    for spiderid in spiderids:

        ### 构造Echarts数据集
        data = dict()
        spider_id = spiderid['id']
        results = PredisctList.objects.filter(spidername=spider_id).extra(select=select).values('minute').annotate(
            sum = Sum('status')).order_by('minute')
        results_count = PredisctList.objects.filter(spidername=spider_id).extra(select=select).values('minute').annotate(
            sum=Count('status')).order_by('minute')

        # print('size',results.__len__())
        # print(spiderid['name'])
        data_acc_list = []
        data_date_list = []


        #####封装数据
        if  results.__len__() == 0:
            continue
        for i in range(len(results)):
            if results_count[i]['sum'] == 0:
                data_acc_list.append(0.0)
            else:
                data_acc_list.append(results[i]['sum']*1.0/results_count[i]['sum']*100)
            data_date_list.append(results[i]['minute'])


        data['data_sum'] = data_acc_list
        data['data_date'] = data_date_list
        data['data_num'] = data_acc_list.__len__()
        data['data_name'] = spiderid['name']
        all_data.append(data)
    Echart_data['data'] = all_data
    Echart_data['count'] =all_data.__len__()
    # print(PredisctList.objects.all().values('spidername').distinct())
    print(Echart_data)