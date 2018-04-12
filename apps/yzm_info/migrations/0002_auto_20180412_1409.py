# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-12 14:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yzm_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='训练集名称')),
                ('path', models.FilePathField(allow_folders=True, verbose_name='数据集路径')),
                ('nums', models.IntegerField(max_length=20, verbose_name='数据集大小')),
                ('ratio', models.FloatField(default='0.25', max_length=20, verbose_name='测试集比例')),
                ('desc', models.TextField(verbose_name='描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '数据集',
                'verbose_name_plural': '数据集',
            },
        ),
        migrations.AddField(
            model_name='yzminfo',
            name='img',
            field=models.ImageField(default='', max_length=200, upload_to='', verbose_name='验证码图片'),
        ),
        migrations.AddField(
            model_name='traindata',
            name='yzmname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yzm_info.YzmInfo', verbose_name='待绑定验证码'),
        ),
    ]
