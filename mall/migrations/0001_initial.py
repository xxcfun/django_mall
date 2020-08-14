# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-08-14 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.SmallIntegerField(choices=[(11, '新闻'), (12, '通知')], default=11, verbose_name='类型')),
                ('title', models.CharField(max_length=255, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('reorder', models.SmallIntegerField(default=0, help_text='数字越大，越靠前', verbose_name='排序')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='生效开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='生效开始时间')),
                ('view_count', models.IntegerField(default=0, verbose_name='浏览次数')),
                ('is_top', models.BooleanField(default=False, verbose_name='是否置顶')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
            ],
            options={
                'db_table': 'system_news',
                'ordering': ['-reorder'],
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='描述')),
                ('types', models.SmallIntegerField(choices=[(11, '首页')], default=11, verbose_name='展现位置')),
                ('img', models.ImageField(upload_to='slider', verbose_name='图片')),
                ('reorder', models.SmallIntegerField(default=0, help_text='数字越大，越靠前', verbose_name='排序')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='生效开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='生效开始时间')),
                ('target_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='跳转地址')),
                ('is_valid', models.BooleanField(default=True, verbose_name='是否删除')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
            ],
            options={
                'db_table': 'system_slider',
                'ordering': ['-reorder'],
            },
        ),
    ]
