
import xadmin
from monitor.models import SpiderInfo, PredisctList, CheckInfo
from .plugins import *


class CheckInfoInline:
    model = CheckInfo
    extra = 0


class SpiderInfoAdmin:

    list_display = ['name','url', 'status','status_tag','run_nums','predict_nums','desc', 'add_time']
    search_fields = ['name','url', 'desc', 'add_time']
    list_filter = ['name','url',  'desc', 'add_time']

    ordering = ['-add_time']

    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    # readonly_fields = ['name','url', 'yzmmodel', 'desc', 'add_time']
    inlines = [CheckInfoInline]
    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(SpiderInfoAdmin, self).queryset()
        return qs

    model_icon = 'fa fa-file-o'

class PredisctListAdmin:

    ###Echarts
    turn_on_Echarts = True

    list_display = ['yzmname',  'image_tag',
                    'predict','status', 'desc', 'add_time']
    search_fields = ['status', 'img',
                    'predict', 'desc', 'add_time']
    list_filter = ['status', 'img',
                    'predict', 'desc', 'add_time']
    #
    ordering = ['-add_time']

    refresh_times = (5,)
    # # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    readonly_fields = ['spidername', 'img',
                    'predict', 'desc', 'add_time']

    model_icon = 'fa fa-file-o'


xadmin.site.register(SpiderInfo, SpiderInfoAdmin)
xadmin.site.register(PredisctList, PredisctListAdmin)