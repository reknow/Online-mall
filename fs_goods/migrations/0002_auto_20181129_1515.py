# Generated by Django 2.1.1 on 2018-11-29 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fs_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='g_pic',
            field=models.ImageField(upload_to='fs_goods/%Y/%m', verbose_name='商品图片'),
        ),
    ]
