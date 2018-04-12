from django.http import request, QueryDict
from django.template.backends import django
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

from GetCap import SaveImg
from bishe.settings import MEDIA_CAP_DB_PATH
from xadmin.views import BaseAdminPlugin, UpdateAdminView, ListAdminView, ModelFormAdminView
import xadmin

class GetCapUrlImgPlugin(BaseAdminPlugin):

    get_pic = False

    def init_request(self, *args, **kwargs):

        print(self.request.POST)
        if  "img" not in self.request.POST:
            print('open')
        else:
            url = self.request.POST['image_url']
            status,path = SaveImg(url)
            if status:
                self.request.POST['img'] = MEDIA_CAP_DB_PATH+path
                print(self.request.POST)
            else:
                pass



xadmin.site.register_plugin(GetCapUrlImgPlugin, ModelFormAdminView)