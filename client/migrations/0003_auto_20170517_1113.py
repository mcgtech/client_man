# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 10:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170517_1109'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='changed_by',
            new_name='modified_by',
        ),
        migrations.RenameField(
            model_name='person',
            old_name='changed_date',
            new_name='modified_date',
        ),
    ]