# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-10 03:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_recipe_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='voted_recipes',
        ),
        migrations.AddField(
            model_name='profile',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='disliked_recipes',
            field=models.ManyToManyField(related_name='profiles_disliked', to='main.Recipe'),
        ),
        migrations.AddField(
            model_name='profile',
            name='liked_recipes',
            field=models.ManyToManyField(related_name='profiles_liked', to='main.Recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredient_list',
            field=models.TextField(),
        ),
    ]
