from django.shortcuts import render

# Create your views here.
from xadmin.sites import site
from xadmin.views import BaseAdminView

class MyAdminView(BaseAdminView):

    def get(self, request, *args, **kwargs):
        pass

site.register_view(r'^test/$', MyAdminView, name='my_test')