from django.template import loader

from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView

REFRESH_VAR = '_refresh'

# 该插件实现了一个列表页面刷新器的效果
class RefreshPlugin(BaseAdminPlugin):

    # 用户可以定制刷新的频率，可以传入多个值。该属性会被 ``OptionClass`` 的同名属性替换
    refresh_times = []

    def init_request(self, *args, **kwargs):
        # 根据用户是否制定了刷新器来决定是否启动该插件
        return bool(self.refresh_times)

    # 插件拦截了返回 Media 的方法，加入自己需要的 js 文件。
    def get_media(self, media):
        if self.request.GET.get(REFRESH_VAR):
            # 放页面处于自动刷新状态时，加入自己的 js 制定刷新逻辑
            media.add_js([self.static('xadmin/js/refresh.js')])
        return media

    # Block Views
    # 在页面中插入 HTML 片段，显示刷新选项。
    def block_top_toolbar(self, context, nodes):
        current_refresh = self.request.GET.get(REFRESH_VAR)
        context.update({
            'has_refresh': bool(current_refresh),
            'clean_refresh_url': self.admin_view.get_query_string(remove=(REFRESH_VAR,)),
            'current_refresh': current_refresh,
            'refresh_times': [{
                'time': r,
                'url': self.admin_view.get_query_string({REFRESH_VAR: r}),
                'selected': str(r) == current_refresh,
            } for r in self.refresh_times],
        })
        # 可以将 HTML 片段加入 nodes 参数中
        nodes.append(loader.render_to_string('xadmin/blocks/refresh.html', context_instance=context))
# 注册插件
site.register_plugin(RefreshPlugin, ListAdminView)