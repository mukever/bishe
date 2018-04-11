
import xadmin
# from TextInputCounter import TextInputCounter
from yzm_info.xadmin_action import MyAction

from .models import YzmInfo,YzmModel



class YzmInfoAdmin:

    list_display = ['name','image_url', 'category', 'tag',
                    'desc', 'add_time']
    search_fields = ['name','image_url', 'category', 'tag',
                    'desc']
    list_filter = ['name','image_url', 'category', 'tag',
                    'desc']

    ordering = ['-add_time']
    # data_charts = {
    #
    #     # "user_count": {'title': u"User Register Raise", "x-field": "add_time", "y-field": ("category",),
    #     #                "order": ('year',)},
    #     # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    # }

    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    #readonly_fields = ['image_url', 'category', 'tag','desc']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(YzmInfoAdmin, self).queryset()
        return qs

    actions = [MyAction]
    model_icon = 'fa fa-user-plus'

class YzmModelAdmin:

    list_display = ['name','yzmname',
                    'desc', 'add_time']
    search_fields = ['name','yzmname',
                    'desc', 'addtime']
    list_filter = ['name','yzmname',
                    'desc', 'add_time']

    ordering = ['-add_time']
    refresh_times = [5, 2]

    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    #readonly_fields = ['image_url', 'category', 'tag','desc']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(YzmModelAdmin, self).queryset()
        return qs

    model_icon = 'fa fa-user-plus'




# xadmin.site.register(PostAdminForm,PostAdmin)
xadmin.site.register(YzmInfo, YzmInfoAdmin)
xadmin.site.register(YzmModel, YzmModelAdmin)

