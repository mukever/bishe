# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-12 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yzminfo', '0005_auto_20180412_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yzminfo',
            name='img',
            field=models.ImageField(blank=True, default='', max_length=200, upload_to='', verbose_name='验证码图片(自动获取)'),
        ),
    ]