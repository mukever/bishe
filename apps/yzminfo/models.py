from django.db import models
from datetime import datetime

# Create your models here.
from bishe import settings
from bishe.settings import MEDIA_URL


class YzmInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='实例名称')
    category = models.CharField(max_length=20, choices=( ('1', '英文数字混合'), ),
                                default='1', verbose_name='类别' )
    tag =models.CharField(max_length=20, choices=( ('1', '1'), ('2', '2') ,('3', '3'),('4', '4'),('5', '5'),('6', '6'),('7', '7'),('8', '8')),
                                default='4', verbose_name='验证码字符个数' )
    desc = models.TextField(verbose_name='描述',blank=True)

    image_url = models.CharField(max_length=300, verbose_name='URL链接')
    img = models.ImageField(max_length=200,verbose_name='验证码图片(自动获取)',default='',blank=True,upload_to='caps/sites/')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '验证码信息'
        verbose_name_plural = verbose_name

    def image_tag(self):
        return u'<img width=100px src="%s%s" />' % (MEDIA_URL, self.img)

    image_tag.short_description = '验证码图片样例(自动获取)'
    image_tag.allow_tags = True

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)
        d = {}
        print(fields)
        import datetime
        for attr in fields:
            if isinstance(getattr(self, attr), datetime.datetime):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(getattr(self, attr), datetime.date):
                d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
            else:
                if attr =='img':
                    d[attr] = self.img.name
                else:
                    d[attr] = getattr(self, attr)

        return d

    def __str__(self):
        return self.name
