# Generated by Django 2.0.3 on 2018-03-31 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20180328_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reserved',
            field=models.PositiveIntegerField(blank=True, default=0, editable=False),
        ),
    ]
