from django.db import models
from datetime import datetime
# Create your models here.

from yzm_info.models import YzmInfo, YzmModel


class SpiderInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='实例名称')
    url = models.ForeignKey(YzmInfo,verbose_name='验证码名称')
    yzmmodel = models.ForeignKey(YzmModel,verbose_name='模型名称')
    desc = models.TextField(verbose_name='描述',blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '爬虫信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class PredisctList(models.Model):
    spidername = models.ForeignKey(YzmInfo,verbose_name='爬虫')
    status = models.CharField(max_length=1, choices=( ('1', '正确'), ('2', '错误') ), default='1', verbose_name='正误' )
    img = models.ImageField(upload_to='img/%Y/%m', verbose_name='验证码图片', max_length=100)
    predict = models.CharField(max_length=50, verbose_name='预测结果')
    desc = models.TextField(verbose_name='备注',blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '预测结果列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.spidername

class SpiderStatus(models.Model):
    spidername = models.ForeignKey(SpiderInfo, verbose_name='实例名称')
    status = models.CharField(max_length=1, choices=( ('1', '开始'), ('2', '结束') ), default='2', verbose_name='状态' )
    desc = models.TextField(verbose_name='备注',blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '爬虫状态'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.spidername
