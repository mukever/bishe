from django.conf.urls import url
from .views import *

urlpatterns = [

    ##cont
    url(r'^spidercontro/(?P<spider_id>\d+)$', SpiderControView.as_view(), name='spidercontro'),
    #
    ##data
    url(r'^predictdata/$', PrediacListDataView.as_view(), name='predictdata'),
    ##data
    url(r'^predict/$', PredictAPI.as_view(), name='predict'),
    #
    # ##yzminfo
    # url(r'^getyzminfo/(?P<yzm_id>\d+)$', GetYzmInfoView.as_view(), name='getyzminfo'),
    #
    # ##yzmpixelinfo
    # url(r'^getyzmpixelinfo/$', GetImgPixelInfoView.as_view(), name='getyzmpixelinfo'),
    #
    # ##yzmcutinfo
    # url(r'^getyzmcutinfo/$', GetImgCutInfoView.as_view(), name='getyzmcutinfo'),
]