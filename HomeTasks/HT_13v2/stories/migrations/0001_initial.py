# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_id', models.CharField(max_length=20)),
                ('score', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=20)),
                ('by', models.CharField(max_length=50)),
                ('title', models.TextField()),
                ('url', models.TextField(default='', null=True)),
                ('text', models.TextField(default='', null=True)),
                ('descendants', models.TextField(default='', null=True)),
                ('kids', models.TextField(default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StoryCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StoryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='story',
            name='story_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.StoryCategory'),
        ),
        migrations.AddField(
            model_name='story',
            name='story_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.StoryType'),
        ),
    ]
