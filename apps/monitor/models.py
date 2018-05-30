from django.conf.urls import url
from django.db import models
from datetime import datetime
# Create your models here.
from bishe.settings import SITE_ROOT, MEDIA_URL
from yzminfo.models import YzmInfo


class SpiderInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='实例名称')
    url = models.ForeignKey(YzmInfo,verbose_name='验证码名称')
    desc = models.TextField(verbose_name='描述',blank=True)
    status = models.CharField(max_length=1, choices=(('1', '正在运行'), ('2', '已经结束')), default='2', verbose_name='当前状态',blank=True)
    run_nums = models.IntegerField(verbose_name='运行次数', default=0,blank=True)
    predict_nums = models.IntegerField(verbose_name='识别次数', default=0,blank=True)
    pid = models.IntegerField(verbose_name='当前运行的线程ID', default=0, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def status_tag(self):
        if self.status == '2':
            meg_info = '启动'
            return u'<a href = "%s"> %s</a>' % (SITE_ROOT + 'api/spidercontro/' + str(self.id), meg_info)
        else:
            meg_info = '终止'

            return meg_info


    status_tag.short_description = '操作'
    status_tag.allow_tags = True


    class Meta:
        verbose_name = '爬虫信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class PredisctList(models.Model):
    spidername = models.ForeignKey(SpiderInfo,verbose_name='爬虫名称')
    yzmname = models.ForeignKey(YzmInfo,verbose_name='验证码名称',blank=True,default='')
    status = models.IntegerField( choices=( (1, '正确'), (0, '错误') ), default=0, verbose_name='正误' )
    img = models.ImageField(upload_to='img/%Y/%m', verbose_name='验证码图片', max_length=100)
    predict = models.CharField(max_length=50, verbose_name='预测结果')
    desc = models.TextField(verbose_name='备注',blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '预测结果列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

    def image_tag(self):
        return u'<img width=100px src="%s%s" />' % (MEDIA_URL, self.img)

    image_tag.short_description = '验证码图片(自动获取)'
    image_tag.allow_tags = True

