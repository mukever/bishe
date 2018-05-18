
import xadmin
from spiderproxy.models import ProxyIPInfo

class ProxyIPAdmin:

    list_display = ['ip', 'add_time']
    search_fields = ['ip', 'add_time']
    list_filter =['ip', 'add_time']

    ordering = ['-add_time']

    #重新在这里写一遍的原因是，避免数据重复
    def queryset(self):
        qs = super(ProxyIPAdmin, self).queryset()
        return qs

    model_icon = 'fa fa-file-o'


xadmin.site.register(ProxyIPInfo, ProxyIPAdmin)
