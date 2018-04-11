
import xadmin
from spider_monitor.models import SpiderInfo, MonitorInfo


class SpiderInfoAdmin:

    list_display = ['name','url', 'yzmmodel', 'desc', 'add_time']
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

    model_icon = 'fa fa-user-plus'

class MonitorInfoAdmin:

    # list_display = ['name','url', 'status', 'img',
    #                 'predict', 'desc', 'add_time']
    # search_fields = ['name','url', 'status', 'img',
    #                 'predict', 'desc', 'add_time']
    # list_filter = ['name','url', 'status', 'img',
    #                 'predict', 'desc', 'add_time']
    #
    # ordering = ['-add_time']

    data_charts = {

        "countss": {'title': u"监控状态", "x-field": ("1990","1991","1992","1993","1994","1995"), "y-field": ("0，1，2，3，4，8",)},
        # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    }

    # # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    # readonly_fields = ['name','url', 'status', 'img',
    #                 'predict', 'desc', 'add_time']
    # #重新在这里写一遍的原因是，避免数据重复
    # def queryset(self):
    #     qs = super(MonitorInfoAdmin, self).queryset()
    #     return qs

    model_icon = 'fa fa-user-plus'

xadmin.site.register(SpiderInfo, SpiderInfoAdmin)
xadmin.site.register(MonitorInfo, MonitorInfoAdmin)

