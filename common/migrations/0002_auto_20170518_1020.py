# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='person',
            name='modified_date',
        ),
    ]
