# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-11 23:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('yzm_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='实例名称')),
                ('status', models.CharField(choices=[('1', '正确'), ('2', '错误')], default='1', max_length=1, verbose_name='正误')),
                ('img', models.ImageField(upload_to='img/%Y/%m', verbose_name='验证码图片')),
                ('predict', models.CharField(max_length=50, verbose_name='预测结果')),
                ('desc', models.TextField(verbose_name='备注')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yzm_info.YzmInfo', verbose_name='爬虫')),
            ],
            options={
                'verbose_name': '监控信息',
                'verbose_name_plural': '监控信息',
            },
        ),
        migrations.CreateModel(
            name='SpiderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='实例名称')),
                ('desc', models.TextField(verbose_name='描述')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yzm_info.YzmInfo', verbose_name='验证码名称')),
                ('yzmmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yzm_info.YzmModel', verbose_name='模型名称')),
            ],
            options={
                'verbose_name': '爬虫信息',
                'verbose_name_plural': '爬虫信息',
            },
        ),
    ]
