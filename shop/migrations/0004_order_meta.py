# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-21 14:04
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20190121_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True, default={}),
        ),
    ]
