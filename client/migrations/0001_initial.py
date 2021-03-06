# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 12:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.Person')),
                ('client_status', models.IntegerField(choices=[(None, 'Please select'), (0, 'Canvass'), (1, 'Closed'), (2, 'Education'), (3, 'Employed'), (4, 'Profile'), (5, 'Waiting List'), (6, 'Work Experience')], default=None, null=True)),
                ('client_group', models.IntegerField(choices=[(None, 'Please select'), (0, 'Autism'), (1, 'Dyspraxia'), (2, 'Head Injury'), (3, 'Learning Difficulties'), (4, 'Low Skilled'), (5, 'Mental Health'), (6, 'No Experience of Work'), (7, 'To Be Assigned'), (8, 'Unemployed (Under 3yrs no health issue)'), (9, 'Young People (NEET)')], default=None)),
                ('client_group_evidence', models.FileField(blank=True, null=True, upload_to='client/group_evid/')),
                ('time_unemployed', models.IntegerField(choices=[(None, 'Please select'), (0, 'Up to 6 months'), (1, '6 - 12 months'), (2, '13 - 24 months'), (3, '25 - 36 months'), (4, 'Over 3 years'), (5, 'TBC'), (6, 'Attending School')], default=None)),
                ('stage', models.IntegerField(choices=[(None, 'Please select'), (0, 'Stage 2'), (1, 'Stage 3'), (3, '18+')], default=None, null=True)),
                ('employment_status', models.IntegerField(choices=[(None, 'Please select'), (0, 'Economically Inactive'), (1, 'Employed (including self-employed)'), (2, 'Long Term Employed'), (3, 'NEET Inactive'), (4, 'Unemployed')], default=None, null=True)),
                ('employment_status_evidence', models.FileField(blank=True, null=True, upload_to='client/emp_state_evid/')),
                ('jsa', models.IntegerField(choices=[(None, 'Please select'), (0, 'No'), (1, 'Yes')], default=None)),
                ('recommended_by', models.IntegerField(choices=[(None, 'Please select'), (0, 'Business Gateway'), (1, 'College'), (2, 'Highland Council Employability team'), (3, 'Jobcentre Plus'), (4, 'Ness Toiletries'), (5, 'NHS'), (6, 'Rag Tag N Textile'), (7, 'Re-registration'), (8, 'School'), (9, 'Shirlie Project'), (10, 'Skills Development Scotland'), (11, 'Social Work'), (12, 'Word of mouth (friend/family)')], default=None)),
                ('education', models.IntegerField(choices=[(None, 'Please select'), (0, 'No qualifications'), (1, 'Access 1 or 2'), (2, 'Access 3 or foundation standard grade'), (3, 'General standard grade or intermediate 1'), (4, 'Credit'), (5, 'Standard grade or intermediate 2'), (6, 'Higher'), (7, 'HNC or advanced Higher'), (8, 'HND or Degree')], default=None)),
                ('sex', models.IntegerField(choices=[(None, 'Please select'), (0, 'Male'), (1, 'Female')], default=None)),
                ('marital_status', models.IntegerField(choices=[(None, 'Please select'), (0, 'Divorced'), (1, 'Married'), (2, 'Separated'), (3, 'Single'), (4, 'TBC'), (5, 'To Be Assigned'), (6, 'Widowed')], default=None)),
                ('ethnicity', models.IntegerField(choices=[(None, 'Please select'), (0, 'Asian (Bangladesh)'), (1, 'Asian (Chinese)'), (2, 'Asian (Indian)'), (3, 'Asian (Other)'), (4, 'Asian (Pakistan)'), (5, 'Black (African)'), (6, 'Black (Caribbean)'), (7, 'Black (Other)'), (8, 'Mixed Background'), (9, 'Other Ethinicity'), (10, 'TBC'), (11, 'Traveller/Gypsy'), (12, 'White (English)'), (13, 'White (Irish)'), (14, 'White (Other)'), (15, 'White (Scottish)'), (16, 'White (Welsh)')], default=None)),
                ('birth_certificate', models.FileField(blank=True, null=True, upload_to='client/birth_certs/')),
                ('social_work_involved', models.BooleanField(default=False)),
                ('ref_received', models.BooleanField(default=False)),
                ('original_client_id', models.IntegerField(default=0)),
                ('nat_ins_number', models.CharField(blank=True, max_length=100)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('common.person',),
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('type', models.IntegerField(choices=[(None, 'Please select'), (0, 'AA'), (1, 'ATW'), (2, 'BP (Autism)'), (3, 'Closed'), (4, 'EF'), (5, 'ESF Tracking'), (6, 'ESF/Lottery Tracking'), (7, 'GRFW'), (8, 'HC'), (9, 'Lottery Tracking'), (10, 'MiR'), (11, 'PP'), (12, 'TIO'), (13, 'WFH'), (14, 'WIO'), (15, 'WP')], default=None)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('referral_date', models.DateField(blank=True, null=True)),
                ('secondary_client_group', models.IntegerField(choices=[(None, 'Please select'), (0, 'Above 54 Years Old'), (1, 'Armed Forces Veteran'), (2, 'Asylum Seeker'), (3, 'Criminal Convictions'), (4, 'Deprived Area'), (5, 'EU Migrant'), (6, 'Homeless Or Threat Of Exclusion'), (7, 'Living In a Jobless Household'), (8, 'Lone Parent'), (9, 'Long Term Unemployed'), (10, 'Low Income Employed'), (11, 'Low Skilled'), (12, 'No Experience Of Work'), (13, 'Primary Carer Of Older Person Over 65'), (14, 'Primary Carer Of Person Under 65'), (15, 'Refugee'), (16, 'Rural Area'), (17, 'Substance Related Issues'), (18, 'To Be Assigned'), (19, 'Underemployed'), (20, 'Young People Leaving Care')], default=None, null=True)),
                ('secondary_client_group_evidence', models.FileField(blank=True, null=True, upload_to='client/group_evid/')),
                ('application_form', models.FileField(blank=True, null=True, upload_to='client/con_app_form/')),
            ],
            options={
                'ordering': ('-start_date', 'created_on'),
            },
        ),
        migrations.CreateModel(
            name='ContractStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Awaiting info man acceptance'), (1, 'Accepted by info man'), (2, 'Approved by fund man'), (3, 'Rejected by fund man'), (4, 'Acceptance revoked by info man'), (5, 'Awaiting fund manager approval'), (6, 'Fund manager approval  undone')], default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('interview_date', models.DateField(blank=True, null=True)),
                ('background_info', models.TextField(blank=True, verbose_name='Background information')),
                ('pref_job_dir', models.TextField(blank=True, verbose_name='Preferred job direction (target outcome)')),
                ('prev_work_exp', models.TextField(blank=True, verbose_name='Previous work experience, including personal feelings on jobs (bullet points)')),
                ('skills', models.TextField(blank=True, verbose_name='Highlight any skills or qualifications client could bring to a job (bullet points)')),
                ('dev_issues', models.TextField(blank=True, verbose_name='Highlight any support or development issues (bullet points):')),
                ('other_comments', models.TextField(blank=True, verbose_name='Other comments/follow up')),
                ('scanned_copy', models.FileField(blank=True, null=True, upload_to='client/init_int/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Learning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning', models.CharField(max_length=300, verbose_name='Other relevant learning/experience/skills')),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='learnings', to='client.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='OtherAgencies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agency', models.IntegerField(choices=[(None, 'Please select'), (0, 'Barnardos'), (1, 'Community Mental Health Team'), (2, 'Department for Work and Pensions'), (3, 'Highland Council Employability'), (4, 'None'), (5, 'Skills Development Scotland'), (6, 'Social Work'), (7, 'Youth Development work')], default=None)),
                ('contact_person', models.CharField(blank=True, max_length=100)),
                ('contact_details', models.CharField(blank=True, max_length=300)),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_agencies', to='client.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='OtherProgrammes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme', models.IntegerField(choices=[(None, 'Please select'), (0, 'AA'), (1, 'ATW'), (2, 'BP (Autism)'), (3, 'Closed'), (4, 'EF'), (5, 'ESF Tracking'), (6, 'ESF/Lottery Tracking'), (7, 'GRFW'), (8, 'HC'), (9, 'Lottery Tracking'), (10, 'MiR'), (11, 'PP'), (12, 'TIO'), (13, 'WFH'), (14, 'WIO'), (15, 'WP')], default=None)),
                ('provider', models.CharField(blank=True, max_length=100)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_programmes', to='client.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training', models.CharField(max_length=300, verbose_name='Planned non-certified training (include any actions taken)')),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planned_training', to='client.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300)),
                ('level', models.CharField(blank=True, max_length=100)),
                ('grade', models.CharField(blank=True, max_length=100)),
                ('date_achieved', models.DateField(blank=True, null=True)),
                ('interview', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='client.Interview')),
            ],
        ),
        migrations.CreateModel(
            name='TIOContract',
            fields=[
                ('contract_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='client.Contract')),
                ('closed_date', models.DateField(blank=True, null=True)),
                ('issue', models.IntegerField(choices=[(None, 'Please select'), (0, 'Learning Difficulty'), (1, 'Autism'), (2, 'Mental Ill Health (3+ yrs, links to CMHT)'), (4, 'Physical and Sensory'), (4, 'Social and Emotional')], default=None, null=True, verbose_name='Adult 18+ with')),
                ('consent_form_complete', models.BooleanField(default=False)),
                ('aa_progress_jsa_18', models.BooleanField(default=False, verbose_name='Progressing from Activity Agreements')),
                ('add_support_jsa_18', models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')),
                ('add_support_jsa_25', models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')),
                ('wca_incapacity', models.BooleanField(default=False, verbose_name='Prior to WCA')),
                ('support_esa', models.BooleanField(default=False, verbose_name='Support Group Category')),
                ('wrag_esa', models.BooleanField(default=False, verbose_name='W.R.A.G (less than 3 months sustained employment in the last 3 yrs)')),
                ('emp_pros_inc', models.BooleanField(default=False, verbose_name='To improve employment prospects')),
                ('other_ben', models.TextField(blank=True, verbose_name='Other Benefits')),
                ('fund_mgr_notes', models.TextField(blank=True, verbose_name='Fund Manager Notes')),
            ],
            options={
                'abstract': False,
            },
            bases=('client.contract',),
        ),
        migrations.AddField(
            model_name='interview',
            name='contract',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interview', to='client.Contract'),
        ),
        migrations.AddField(
            model_name='interview',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interview_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interview',
            name='interviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='interview',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interview_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractstatus',
            name='contract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_status', to='client.Contract'),
        ),
        migrations.AddField(
            model_name='contractstatus',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contractstatus_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contractstatus',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contractstatus_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='client.Client'),
        ),
        migrations.AddField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='job_coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_coach', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contract_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tio_contract', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='latest_contract',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Client', to='client.Contract'),
        ),
    ]
