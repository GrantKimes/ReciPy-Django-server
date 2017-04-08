# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-08 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20170408_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='saved_recipes',
            field=models.ManyToManyField(related_name='profiles_saved', to='main.Recipe'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='voted_recipes',
            field=models.ManyToManyField(related_name='profiles_voted', through='main.RecipeVote', to='main.Recipe'),
        ),
    ]
