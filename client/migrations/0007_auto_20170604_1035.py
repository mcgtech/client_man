# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 10:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_auto_20170604_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='background_info',
            field=models.TextField(blank=True, verbose_name='Background information'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='dev_issues',
            field=models.TextField(blank=True, verbose_name='Highlight any support or development issues (bullet points):'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='other_comments',
            field=models.TextField(blank=True, verbose_name='Other comments/follow up'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='pref_job_dir',
            field=models.TextField(blank=True, verbose_name='Preferred job direction (target outcome)'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='prev_work_exp',
            field=models.TextField(blank=True, verbose_name='Previous work experience, including personal feelings on jobs (bullet points)'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='skills',
            field=models.TextField(blank=True, verbose_name='Highlight any skills or qualifications client could bring to a job (bullet points)'),
        ),
    ]
