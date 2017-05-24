# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20170523_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='secondary_client_group',
            field=models.IntegerField(choices=[(None, 'Please select'), (0, 'Above 54 Years Old'), (1, 'Armed Forces Veteran'), (2, 'Asylum Seeker'), (3, 'Criminal Convictions'), (4, 'Deprived Area'), (5, 'EU Migrant'), (6, 'Homeless Or Threat Of Exclusion'), (7, 'Living In a Jobless Household'), (8, 'Lone Parent'), (9, 'Long Term Unemployed'), (10, 'Low Income Employed'), (11, 'Low Skilled'), (12, 'No Experience Of Work'), (13, 'Primary Carer Of Older Person Over 65'), (14, 'Primary Carer Of Person Under 65'), (15, 'Refugee'), (16, 'Rural Area'), (17, 'Substance Related Issues'), (18, 'To Be Assigned'), (19, 'Underemployed'), (20, 'Young People Leaving Care')], default=None, null=True),
        ),
    ]