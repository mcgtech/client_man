# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 08:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_live_contract'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='live_contract',
            new_name='latest_contract',
        ),
    ]