import datetime
import json

from django.db.models import Sum, Count
from django.template import loader
from django.template.defaultfilters import urlencode
from django.utils.translation import ugettext

from spider_monitor.models import PredisctList, SpiderInfo
from xadmin.plugins.utils import get_context_dict
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ModelAdminView


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def getEchartsData():
    select = {'minute': "CAST(DATE_FORMAT(add_time, '%%Y-%%m-%%d %%H-%%i--01') AS DATETIME)"}
    # print(select)
    # select data
    Echart_data = dict()

    spiderids   = SpiderInfo.objects.values('id', 'name')
    All_data = []
    for spiderid in spiderids:

        ### 构造Echarts数据集
        data = dict()
        spider_id = spiderid['id']
        results = PredisctList.objects.filter(spidername=spider_id).extra(select=select).values('minute').annotate(
            sum=Sum('status'))
        all_results = (PredisctList.objects.filter(spidername=spider_id).extra(select=select).values('minute').annotate(
            sum=Count('status')))
        # print('size',results.__len__())
        # print(spiderid['name'])
        data_sum_list = []
        data_date_list = []

        all_data_sum_list = []
        all_data_date_list = []

        #####封装数据
        if results.__len__() == 0:
            continue
        for result in results:
            data_sum_list.append(result['sum'])
            data_date_list.append(result['minute'])

        for result in all_results:
            all_data_sum_list.append(result['sum'])
            all_data_date_list.append(result['minute'])

        # print(data_sum_list)
        # print(data_date_list)
        # print(all_data_sum_list)
        # print(all_data_date_list)
        #
        # print([ data_sum_list[i]/all_data_sum_list[i]*100 for i in range(len(data_sum_list)) ])

        point_data = [ data_sum_list[i]/all_data_sum_list[i]*100 for i in range(len(data_sum_list)) ]

        data['data_sum'] = point_data
        data['data_date'] = data_date_list
        data['spider_name'] = spiderid['name']
        All_data.append(data)
    Echart_data['data'] = All_data
    Echart_data['count'] = All_data.__len__()

    Echart_data_json = json.dumps(Echart_data,cls=CJsonEncoder)
    print(Echart_data_json)
    ds = json.dumps(Echart_data_json)
    print("ds type:", type(ds), "ds:", ds)
    l = json.loads(ds)
    print(l)
    return Echart_data_json


class EChartsPlugin(BaseAdminPlugin):

    turn_on_Echarts = False

    def init_request(self, *args, **kwargs):
        return bool(self.turn_on_Echarts)

    def get_chart_url(self, name, v):
        return self.admin_view.model_admin_url('chart', name) + self.admin_view.get_query_string()

    # Media
    def get_media(self, media):
        media.add_js(['/media/plugins/echarts/js/echarts.min.js'])
        return media

    # Block Views
    def block_results_top(self, context, nodes):
        context.update({
            'Echarts_Title': "预测结果",
            'Echarts_Data': getEchartsData(),
        })


        nodes.append(loader.render_to_string('plugins/echarts/echarts.html',
                                             context=get_context_dict(context)))


# 注册插件
site.register_plugin(EChartsPlugin, ModelAdminView)