# Generated by Django 2.0.3 on 2018-03-25 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20180325_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ManyToManyField(blank=True, related_name='products', to='product.Subcategory'),
        ),
    ]