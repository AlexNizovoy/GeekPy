# Generated by Django 2.0.4 on 2018-04-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20180401_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='on_main',
            field=models.BooleanField(default=False),
        ),
    ]
