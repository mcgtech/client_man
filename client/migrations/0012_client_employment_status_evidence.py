# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_client_client_group_evidence'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='employment_status_evidence',
            field=models.FileField(blank=True, null=True, upload_to='client/emp_state_evid/'),
        ),
    ]
