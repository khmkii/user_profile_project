# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20161121_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.FilePathField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='biography',
            field=models.TextField(default=''),
        ),
    ]
