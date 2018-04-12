from django.db import models
from datetime import datetime

# Create your models here.
from bishe.settings import MEDIA_URL


class YzmInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='实例名称')
    category = models.CharField(max_length=20, choices=( ('1', '纯英文字符'), ('2', '纯数字字符'), ('3', '英文数字混合') ),
                                default='1', verbose_name='类别' )
    tag =models.CharField(max_length=20, choices=( ('1', '可切割'), ('2', '不可切割') ),
                                default='1', verbose_name='是否可切割' )
    desc = models.TextField(verbose_name='描述',blank=True)

    image_url = models.CharField(max_length=50, verbose_name='URL链接')
    img = models.ImageField(max_length=200,verbose_name='验证码图片(自动获取)',default='',blank=True,upload_to='caps/sites/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码信息'
        verbose_name_plural = verbose_name

    def image_tag(self):
        return u'<img width=100px src="%s%s" />' % (MEDIA_URL, self.img)

    image_tag.short_description = '验证码图片(自动获取)'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name


class YzmModel(models.Model):
    name = models.CharField(max_length=50, verbose_name='模型名称')
    yzmname = models.ForeignKey(YzmInfo,verbose_name='验证码信息')
    desc = models.TextField(verbose_name='描述',blank=True)

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码模型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class TrainData(models.Model):
    name = models.CharField(max_length=50, verbose_name='训练集名称')
    yzmname = models.ForeignKey(YzmInfo,verbose_name='待绑定验证码')
    path = models.FilePathField(allow_folders=True,verbose_name='数据集路径')
    nums = models.IntegerField(verbose_name='数据集大小')
    ratio = models.FloatField(max_length=20,verbose_name='测试集比例',default='0.25')
    #还有其他属性待 完成，目前就这几个。。。。 够中期答辩就行
    desc = models.TextField(verbose_name='描述',blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '数据集'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name