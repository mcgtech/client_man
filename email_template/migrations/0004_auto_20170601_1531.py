# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 15:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('email_template', '0003_auto_20170601_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailtemplate',
            old_name='to_address',
            new_name='to_addresses',
        ),
    ]