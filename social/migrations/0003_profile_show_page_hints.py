# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 19:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_auto_20170324_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_page_hints',
            field=models.BooleanField(default=True),
        ),
    ]
