"""bishe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.views.static import serve #处理静态文件
from bishe.settings import MEDIA_ROOT

import xadmin

from apps.api.views import *

urlpatterns = [

    url('admin/', xadmin.site.urls),
    url(r'^predict/$', predict),
    url(r'^huilianwang/$', huilianwang),
    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]
from bishe.settings import STATIC_ROOT, MEDIA_ROOT
# 配置静态文件访问处理
urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}))
urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}))

# if settings.DEBUG:
#     # debug_toolbar 插件配置
#     import debug_toolbar
#     urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
# else:
#     # 项目部署上线时使用
#     from bishe.settings import STATIC_ROOT, MEDIA_ROOT
#
#     # 配置静态文件访问处理
#     urlpatterns.append(url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}))
#     urlpatterns.append(url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}))