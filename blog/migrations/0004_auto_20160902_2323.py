# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-02 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160902_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poetsgroup',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
