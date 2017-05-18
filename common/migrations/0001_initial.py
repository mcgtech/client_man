# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-18 17:51
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
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Client'), (1, 'Job Coach'), (2, 'Manager'), (3, 'Partner')], default=0)),
                ('title', models.IntegerField(choices=[(0, 'Mr'), (1, 'Mrs'), (2, 'Miss'), (3, 'Ms')], default=0)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('known_as', models.CharField(blank=True, max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('forename', models.CharField(blank=True, max_length=100)),
                ('surname', models.CharField(blank=True, max_length=100)),
                ('email_address', models.CharField(blank=True, max_length=100)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
