# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-17 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.BinaryField()),
                ('name', models.CharField(max_length=200)),
                ('blurb', models.CharField(max_length=200)),
                ('goal', models.CharField(max_length=200)),
                ('pledged', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('usd_pledged', models.FloatField()),
            ],
        ),
    ]
