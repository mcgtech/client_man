from django.db import models
from common.models import Auditable
from .client import Client
from django.conf import settings

class Contract(Auditable):
    AA = 0
    ATW = 1
    BP = 2
    CON_CLOSE = 3
    EF = 4
    ESF = 5
    ESF_LOTT = 6
    GRFW = 7
    HC = 8
    LOTT = 9
    MIR = 10
    PP = 11
    TIO = 12
    WFH = 13
    WIO = 14
    WP = 15
    TYPES = (
        (None, 'Please select'),
        (AA, 'AA'),
        (ATW, 'ATW'),
        (BP, 'BP (Autism)'),
        (CON_CLOSE, 'Closed'),
        (EF, 'EF'),
        (ESF, 'ESF Tracking'),
        (ESF_LOTT, 'ESF/Lottery Tracking'),
        (GRFW, 'GRFW'),
        (HC, 'HC'),
        (LOTT, 'Lottery Tracking'),
        (MIR, 'MiR'),
        (PP, 'PP'),
        (TIO, 'TIO'),
        (WFH, 'WFH'),
        (WIO, 'WIO'),
        (WP, 'WP'),
    )
    ABOVE_54 = 0
    ARM_FORCE = 1
    ASY_SEEK = 2
    CRIM_CON = 3
    DEP_AREA = 4
    EU_MIG = 5
    HOMELESS = 6
    IN_JOBLESS_HOUSE = 7
    LONE_PAR = 8
    LT_UNEMP = 9
    LI_EMP = 10
    LOW_SKILL = 11
    NO_EXP_WORK = 12
    PC_OVER_65 = 13
    PC_UNDER_65 = 14
    REFUGEE = 15
    RURAL = 16
    SR_ISS = 17
    TO_BE = 18
    UNDER = 19
    YP_LV_CARE = 20
    SEC_CLIENT_GROUPS = (
        (None, 'Please select'),
        (ABOVE_54, 'Above 54 Years Old'),
        (ARM_FORCE, 'Armed Forces Veteran'),
        (ASY_SEEK, 'Asylum Seeker'),
        (CRIM_CON, 'Criminal Convictions'),
        (DEP_AREA, 'Deprived Area'),
        (EU_MIG, 'EU Migrant'),
        (HOMELESS, 'Homeless Or Threat Of Exclusion'),
        (IN_JOBLESS_HOUSE, 'Living In a Jobless Household'),
        (LONE_PAR, 'Lone Parent'),
        (LT_UNEMP, 'Long Term Unemployed'),
        (LI_EMP, 'Low Income Employed'),
        (LOW_SKILL, 'Low Skilled'),
        (NO_EXP_WORK, 'No Experience Of Work'),
        (PC_OVER_65, 'Primary Carer Of Older Person Over 65'),
        (PC_UNDER_65, 'Primary Carer Of Person Under 65'),
        (REFUGEE, 'Refugee'),
        (RURAL, 'Rural Area'),
        (SR_ISS, 'Substance Related Issues'),
        (TO_BE, 'To Be Assigned'),
        (UNDER, 'Underemployed'),
        (YP_LV_CARE, 'Young People Leaving Care'),
    )
    type = models.IntegerField(choices=TYPES, default=None)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    referral_date = models.DateField(null=True, blank=True)
    secondary_client_group = models.IntegerField(choices=SEC_CLIENT_GROUPS, default=None, null=True)
    secondary_client_group_evidence = models.FileField(upload_to='client/group_evid/', blank=True, null=True)
    application_form = models.FileField(upload_to='client/con_app_form/', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="contract")

    def get_link(self):
        url = self.get_absolute_url()
        link = '<a target="_blank" href="' + url + '">' + self.get_type_display() + '</a>'
        start = self.start_date.strftime(settings.DISPLAY_DATE) if self.start_date is not None else ''
        latest_status = self.contract_status.all().order_by('modified_on').first()
        status = '' if latest_status is None else ' (' + latest_status.get_status_display() + ' )'
        end = (' to ' + self.end_date.strftime(settings.DISPLAY_DATE)) if self.end_date is not None else ''

        return link + ' ' + start + end + status

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('contract_edit', args=[str(self.client.id), str(self.id)])

    def get_all_status_as_list(self):
        table = '<table >'
        for status in self.contract_status.all().order_by('modified_on'):
            table = table + '<tr>' + '<td>'
            table = table + status.get_summary()
            table = table + '</td>' + '</tr>'
        table = table + '</table>'

        return table

    def __str__(self):
       start_date = '' if self.start_date is None else self.start_date.strftime(settings.DISPLAY_DATE)
       return '' if self.client is None else self.client.get_full_name() + ', type: '+ self.get_type_display() + ', start date - ' + start_date


class TIOContract(Contract):
    LD = 0
    AU = 1
    MENT_ILL = 2
    REJ_FUND_MAN = 3
    PH_SEN = 4
    SOC_EM = 4
    ISSUES = (
        (None, 'Please select'),
        (LD, 'Learning Difficulty'),
        (AU, 'Autism'),
        (MENT_ILL, 'Mental Ill Health (3+ yrs, links to CMHT)'),
        (PH_SEN, 'Physical and Sensory'),
        (SOC_EM, 'Social and Emotional'),
    )
    issue = models.IntegerField(choices=ISSUES, default=None, verbose_name='Adult 18+ with', null=True)
    consent_form_complete = models.BooleanField(default=False)
    aa_progress_jsa_18 = models.BooleanField(default=False, verbose_name='Progressing from Activity Agreements')
    add_support_jsa_18 = models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')
    add_support_jsa_25 = models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')
    wca_incapacity = models.BooleanField(default=False, verbose_name='Prior to WCA')
    support_esa = models.BooleanField(default=False, verbose_name='Support Group Category')
    wrag_esa = models.BooleanField(default=False, verbose_name='W.R.A.G (less than 3 months sustained employment in the last 3 yrs)')
    emp_pros_inc = models.BooleanField(default=False, verbose_name='To improve employment prospects')
    other_ben = models.TextField(verbose_name='Other Benefits')
    fund_mgr_notes = models.TextField(verbose_name='Fund Manager Notes')


class ContractStatus(Auditable):
    AWAIT_INF_MAN_APP = 0
    AWAIT_FUND_MAN_APP = 1
    APP_FUND_MAN = 2
    REJ_FUND_MAN = 3
    ACC_INFO_MAN = 4
    STATUS = (
        (AWAIT_INF_MAN_APP, 'Awaiting info man approval'),
        (AWAIT_FUND_MAN_APP, 'Awaiting fund man approval'),
        (APP_FUND_MAN, 'Approved by fund man'),
        (REJ_FUND_MAN, 'Rejected by fund man'),
        (ACC_INFO_MAN, 'Accepted by info man'),
    )
    status = models.IntegerField(choices=STATUS, default=AWAIT_INF_MAN_APP)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="contract_status")

    def get_summary(self):
        return self.get_status_display() + ' - ' + self.modified_on.strftime(settings.DISPLAY_DATE_TIME)

    def __str__(self):
       return self.get_status_display() + ' - ' + str(self.contract)
