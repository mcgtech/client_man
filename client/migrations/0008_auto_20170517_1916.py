# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 18:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_comment_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='note',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='person',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]