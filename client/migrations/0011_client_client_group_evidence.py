# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20170522_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='client_group_evidence',
            field=models.FileField(blank=True, null=True, upload_to='client/group_evid/'),
        ),
    ]