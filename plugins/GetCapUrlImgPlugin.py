from django.http import request, QueryDict
from django.template.backends import django
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from .GetCap import SaveImg
from bishe.settings import MEDIA_CAP_DB_PATH

import xadmin
from xadmin import forms
from xadmin.views import BaseAdminPlugin, ListAdminView, ModelFormAdminView, UpdateAdminView, DetailAdminView, \
    filter_hook, CreateAdminView


class GetCapUrlImgPlugin(BaseAdminPlugin):

    get_pic = False

    def init_request(self, *args, **kwargs):

        # if  "img" not in self.request.POST:
        #     print('open')
        # else:
        #     url = self.request.POST['image_url']
        #     status,path = SaveImg(url)
        #     if status:
        #         self.request.POST['img'] = MEDIA_CAP_DB_PATH+path
        #         print(self.request.POST)
        #     else:
        #         pass
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


xadmin.site.register_plugin(GetCapUrlImgPlugin, UpdateAdminView)
xadmin.site.register_plugin(CreateCapUrlImgPlugin, CreateAdminView)



