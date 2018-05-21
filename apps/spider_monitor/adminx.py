
import xadmin
from spider_monitor.models import SpiderInfo, PredisctList, SpiderStatus
from .plugins import *

class SpiderInfoAdmin:

    list_display = ['name','url', 'yzmmodel','status','status_tag','run_nums','predict_nums','desc', 'add_time']
    search_fields = ['name','url', 'yzmmodel', 'desc', 'add_time']
    list_filter = ['name','url', 'yzmmodel', 'desc', 'add_time']

    ordering = ['-add_time']
    # data_charts = {
    #
    #     "user_count": {'title': u"User Register Raise", "x-field": "year", "y-field": ("cn",),
    #                    "order": ('year',)},
    #     "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }

    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    # readonly_fields = ['name','url', 'yzmmodel', 'desc', 'add_time']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(SpiderInfoAdmin, self).queryset()
        return qs

    model_icon = 'fa fa-file-o'

class PredisctListAdmin:


    ###Echarts
    turn_on_Echarts = True

    list_display = ['yzmname','spidername',  'image_tag',
                    'predict','status', 'desc', 'add_time']
    search_fields = ['spidername', 'status', 'img',
                    'predict', 'desc', 'add_time']
    list_filter = ['spidername', 'status', 'img',
                    'predict', 'desc', 'add_time']
    #
    ordering = ['-add_time']

    refresh_times = (5,)
    # # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    readonly_fields = ['spidername', 'status', 'img',
                    'predict', 'desc', 'add_time']

    model_icon = 'fa fa-file-o'


# class SpiderStatusAdmin:
#
#     #getdata
#
#     data_charts = {
#
#         "spider_monitor": {'title': u"监控状态", "x-field": 'spidername', "y-field": ('ratio_nums'),"order":('add_time')},
#         # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
#     }
#     refresh_times = (5,)
#     # # readonly_fields 和 exclude 的字段不要重复，否则会冲突
#     # readonly_fields = ['name','url', 'status', 'img',
#     #                 'predict', 'desc', 'add_time']
#     # #重新在这里写一遍的原因是，避免数据重复
#     # def queryset(self):
#     #     qs = super(MonitorInfoAdmin, self).queryset()
#     #     return qs
#
#     model_icon = 'fa fa-file-o'

xadmin.site.register(SpiderInfo, SpiderInfoAdmin)
xadmin.site.register(PredisctList, PredisctListAdmin)
# xadmin.site.register(SpiderStatus, SpiderStatusAdmin)