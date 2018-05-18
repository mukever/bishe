from django.http import request, QueryDict
from django.template.backends import django
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.template import loader

from xadmin.plugins.utils import get_context_dict
from .untils import SaveImg
from bishe.settings import MEDIA_CAP_DB_PATH

import xadmin
from xadmin import forms
from xadmin.views import BaseAdminPlugin, ListAdminView, ModelFormAdminView, UpdateAdminView, DetailAdminView, \
    filter_hook, CreateAdminView, ModelAdminView


class GetCapUrlImgPlugin(BaseAdminPlugin):

    get_pic = False

    def init_request(self, *args, **kwargs):

        return bool(self.get_pic)

    def get_form_datas(self,params,*arg,**kwargs):
        if "img" not in self.request.POST:
            pass
        else:
            # print(params['instance'].img)
            # print(type(params['instance']))
            url = self.request.POST['image_url']
            name = self.request.POST['name']
            status, path = SaveImg(url, name)
            if status:

                old_path = params['instance'].img
                print(old_path)
                params['instance'].img = MEDIA_CAP_DB_PATH+path
                print(params['instance'].img)
        return params

class CreateCapUrlImgPlugin(BaseAdminPlugin):

    create_get_pic = False

    def init_request(self, *args, **kwargs):

        return bool(self.create_get_pic)

    def get_form_datas(self,params,*arg,**kwargs):
        if "img" not in self.request.POST:
            # print(params)
            pass
        else:
            url = self.request.POST['image_url']
            name = self.request.POST['name']
            status, path = SaveImg(url,name)
            print(params)
            if status:
                old_path = params['data']['img']
                print(old_path)
                params['data']['img'] = MEDIA_CAP_DB_PATH + path
                print(params['data']['img'])
        return params

#自动获取验证码图片插件
xadmin.site.register_plugin(GetCapUrlImgPlugin, UpdateAdminView)
xadmin.site.register_plugin(CreateCapUrlImgPlugin, CreateAdminView)


#构建创建模型的页面
class CreateModelPlugin(BaseAdminPlugin):

    turn_on_CreateModel = False

    def init_request(self, *args, **kwargs):
        return bool(self.turn_on_CreateModel)


    # # Media
    # def get_media(self, media):
    #
    #     return media

    # Block Views
    def block_results_top(self, context, nodes):
        context.update({
        })
        nodes.append(loader.render_to_string('plugins/models/models.html',
                                             context=get_context_dict(context)))

xadmin.site.register_plugin(CreateModelPlugin, ModelAdminView)