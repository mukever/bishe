from django.conf.urls import url
from .views import *

urlpatterns = [

    ##cont
    url(r'^spidercontro/(?P<spider_id>\d+)$', SpiderControView.as_view(), name='spidercontro'),

    ##data
    url(r'^predictdata/$', PrediacListDataView.as_view(), name='predictdata'),

]