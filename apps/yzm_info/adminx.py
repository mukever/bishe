import xadmin
# from TextInputCounter import TextInputCounter
from .plugins import *
from .models import YzmInfo, YzmModel, TrainData


class YzmInfoAdmin(object):

    get_pic = True
    create_get_pic = True
    list_display = ['name','image_url','image_tag', 'category', 'tag',
                    'desc', 'add_time']
    search_fields = ['name','image_url', 'category', 'tag',
                    'desc']
    list_filter = ['name','image_url', 'category', 'tag',
                    'desc']

    ordering = ['-add_time']
    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    # readonly_fields = ['img']
    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(YzmInfoAdmin, self).queryset()
        return qs

    # def save_models(self):
    #     self.new_obj.yzminfo = self.request.yzminfo
    #     super().save_models()

    # actions = [MyAction]
    plugins = [GetCapUrlImgPlugin]
    refresh_times = (3, 5)
    model_icon = 'fa fa-handshake-o'

class YzmModelAdmin:
    # get_pic = True
    list_display = ['name','yzmname',
                    'desc', 'add_time']
    search_fields = ['name','yzmname',
                    'desc', 'addtime']
    list_filter = ['name','yzmname',
                    'desc', 'add_time']

    ordering = ['-add_time']

    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    # readonly_fields = ['image_url', 'category', 'tag','desc']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(YzmModelAdmin, self).queryset()
        return qs

    model_icon = 'fa fa-file-o'


class TrainDataAdmin:
    # get_pic = True
    list_display = ['name','yzmname','path','nums','ratio',
                    'desc', 'add_time']
    search_fields =  ['name','yzmname','path','nums','ratio',
                    'desc', 'add_time']
    list_filter = ['name','yzmname','path','nums','ratio',
                    'desc', 'add_time']

    ordering = ['-add_time']


    # readonly_fields 和 exclude 的字段不要重复，否则会冲突
    #readonly_fields = ['image_url', 'category', 'tag','desc']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(TrainDataAdmin, self).queryset()
        return qs

    save_on_top = False
    model_icon = 'fa fa-file-o'


xadmin.site.register(YzmInfo, YzmInfoAdmin)
xadmin.site.register(YzmModel, YzmModelAdmin)
xadmin.site.register(TrainData,TrainDataAdmin)
