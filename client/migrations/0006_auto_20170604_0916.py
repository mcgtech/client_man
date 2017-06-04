# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_auto_20170604_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interview',
            old_name='start_date',
            new_name='interview_date',
        ),
        migrations.AddField(
            model_name='interview',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='client.Client'),
        ),
    ]