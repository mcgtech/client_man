# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 11:51
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
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_1', models.CharField(blank=True, max_length=100)),
                ('line_2', models.CharField(blank=True, max_length=100)),
                ('line_3', models.CharField(blank=True, max_length=100)),
                ('post_code', models.CharField(blank=True, max_length=100)),
                ('area', models.IntegerField(choices=[(None, 'Please select'), (0, 'Badenoch and Strathspey'), (1, 'Caithness'), (2, 'Inverness and Nairn'), (3, 'Lochaber'), (4, 'Ross-shire'), (5, 'Skye'), (6, 'Sutherland')], default=None)),
                ('evidence', models.FileField(blank=True, upload_to='client/address_evidence/')),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField()),
                ('modified_date', models.DateTimeField(blank=True, null=True)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(None, 'Please select'), (0, 'Client'), (1, 'Job Coach'), (2, 'Manager'), (3, 'Partner')], default=None)),
                ('title', models.IntegerField(choices=[(None, 'Please select'), (0, 'Mr'), (1, 'Mrs'), (2, 'Miss'), (3, 'Ms')], default=None)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('known_as', models.CharField(blank=True, max_length=100)),
                ('dob', models.DateField(blank=True, null=True)),
                ('forename', models.CharField(blank=True, max_length=100)),
                ('surname', models.CharField(blank=True, max_length=100)),
                ('email_address', models.CharField(blank=True, max_length=100)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person_modified_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Telephone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(None, 'Please select'), (0, 'Home'), (1, 'Mobile'), (2, 'Parents'), (3, 'Work')], default=None)),
                ('number', models.CharField(blank=True, max_length=100)),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='telephone', to='common.Person')),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='note', to='common.Person'),
        ),
        migrations.AddField(
            model_name='address',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address', to='common.Person'),
        ),
    ]
