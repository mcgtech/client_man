# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-02 13:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('template_identifier', models.IntegerField(choices=[(None, 'Please select'), (0, 'Contract accept'), (1, 'Contract revoke'), (2, 'Contract approve'), (3, 'Contract reject')], default=None, unique=True)),
                ('subject', models.CharField(max_length=100)),
                ('from_address', models.CharField(max_length=100)),
                ('to_addresses', models.TextField()),
                ('cc_addresses', models.TextField(blank=True)),
                ('bcc_addresses', models.TextField(blank=True)),
                ('plain_body', models.TextField(help_text='This will be used if recipients software can not handle html')),
                ('html_body', models.TextField(help_text='This will be used if recipients software can handle html')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emailtemplate_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emailtemplate_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
