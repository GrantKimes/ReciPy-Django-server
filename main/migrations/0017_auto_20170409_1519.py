# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-09 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20170408_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='source',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='time_in_seconds',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='yummly_image_url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='yummly_url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
