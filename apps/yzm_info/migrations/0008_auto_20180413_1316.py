# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-13 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yzm_info', '0007_auto_20180412_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yzminfo',
            name='image_url',
            field=models.CharField(max_length=300, verbose_name='URL链接'),
        ),
    ]