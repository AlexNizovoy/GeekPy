# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-11 10:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20180210_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='date_finish',
            field=models.DateTimeField(default=''),
        ),
    ]
