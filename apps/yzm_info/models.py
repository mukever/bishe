from django.db import models
from datetime import datetime

# Create your models here.
class YzmInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='实例名称')
    category = models.CharField(max_length=20, choices=( ('1', '纯英文字符'), ('2', '纯数字字符'), ('3', '英文数字混合') ),
                                default='1', verbose_name='类别' )
    tag =models.CharField(max_length=20, choices=( ('1', '可切割'), ('2', '不可切割') ),
                                default='1', verbose_name='是否可切割' )
    desc = models.TextField(verbose_name='描述')

    image_url = models.CharField(max_length=50, verbose_name='URL链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class YzmModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='模型名称')
    yzmname = models.ForeignKey(YzmInfo,verbose_name='验证码信息')
    desc = models.TextField(verbose_name='描述')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码模型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name