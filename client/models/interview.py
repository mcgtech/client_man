from django.db import models
from common.models import Auditable
from .client import Contract
from django.conf import settings

class Interview(Auditable):
    # https://www.webforefront.com/django/setuprelationshipsdjangomodels.html
    interviewer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='interviews', limit_choices_to={'groups__name': settings.JOB_COACH})
    interview_date = models.DateField(null=True, blank=True)
    background_info = models.TextField(verbose_name='Background information', blank=True)
    pref_job_dir = models.TextField(verbose_name='Preferred job direction (target outcome)', blank=True)
    prev_work_exp = models.TextField(verbose_name='Previous work experience, including personal feelings on jobs (bullet points)', blank=True)
    skills = models.TextField(verbose_name='Highlight any skills or qualifications client could bring to a job (bullet points)', blank=True)
    dev_issues = models.TextField(verbose_name='Highlight any support or development issues (bullet points):', blank=True)
    other_comments = models.TextField(verbose_name='Other comments/follow up', blank=True)
    scanned_copy = models.FileField(upload_to='client/init_int/', blank=True, null=True)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, related_name="interviews")


class Qualification(models.Model):
    title = models.CharField(max_length=300, blank=True)
    level = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=100, blank=True)
    date_achieved = models.DateField(null=True, blank=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, related_name="qualifications")


class Learning(models.Model):
    learning = models.TextField(verbose_name='Other relevant learning/experience/skills')
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, related_name="learnings")


class PlannedTraining(models.Model):
    training = models.TextField(verbose_name='Planned non-certified training (include any actions taken)')
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, related_name="planned_training")


class OtherAgencies(models.Model):
    BARN = 0
    COMM_MEN = 1
    DWP = 2
    HCE = 3
    NONE = 4
    SDS = 5
    SW = 6
    YDW = 7
    AGENCIES = (
        (None, 'Please select'),
        (BARN, 'Barnardos'),
        (COMM_MEN, 'Community Mental Health Team'),
        (DWP, 'Department for Work and Pensions'),
        (HCE, 'Highland Council Employability'),
        (NONE, 'None'),
        (SDS, 'Skills Development Scotland'),
        (SW, 'Social Work'),
        (YDW, 'Youth Development work'),
    )
    agency = models.IntegerField(choices=AGENCIES, default=None)
    contact_person = models.TextField()
    contact_details = models.TextField()
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, related_name="other_agencies")


class OtherProgrammes(models.Model):
    programme = models.IntegerField(choices=Contract.TYPES, default=None)
    provider = models.TextField()
    end_date = models.CharField(max_length=100, blank=True)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, related_name="other_programmes")