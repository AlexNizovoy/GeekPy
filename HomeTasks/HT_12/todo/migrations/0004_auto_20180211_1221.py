# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20180211_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_finish',
            field=models.DateTimeField(blank=True),
        ),
    ]
