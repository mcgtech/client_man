from django.db import models
from common.models import Auditable
# from .client import Client
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
    FULL_TYPES = {AA: 'AA',
                ATW : 'ATW',
                BP : 'BP Autism)',
                CON_CLOSE : 'Closed',
                EF : 'EF',
                ESF : 'ESF Tracking',
                ESF_LOTT : 'ESF/Lottery Tracking',
                GRFW : 'GRFW',
                HC : 'HC',
                LOTT : 'Lottery Tracking',
                MIR : 'MiR',
                PP : 'PP',
                TIO : 'Try It Out',
                WFH : 'WFH',
                WIO : 'WIO',
                WP : 'WP'}
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
    # https://www.webforefront.com/django/setuprelationshipsdjangomodels.html
    # a job coach can have many clients, but a client can have only one coach, so in django we add the ForeignKey to the many part of the relationship:
    job_coach = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_coach', blank=True, null=True, limit_choices_to={'groups__name': settings.JOB_COACH})
    # if I make it OneToOneField then I get duplicate key error
    # partner = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, related_name='tio_contract')
    # I moved this from TIO as other contracts like tio may need it but mainly because I need to query partner on the base class
    partner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tio_contract', blank=True, null=True, limit_choices_to={'groups__name__in': [settings.HI_COUNCIL_PART, settings.RAG_TAG_PART]})
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, related_name="contract")

    def contract_has_a_partner(self):
        return self.type == Contract.TIO

    def get_latest_status(self):
        return self.get_ordered_status().first()

    def get_latest_status_with_state(self, status):
        return self.get_ordered_status().filter(status=status).first()

    def get_ordered_status(self):
        return self.contract_status.all().order_by('-modified_on')

    def get_summary(self, type_as_link):
        url = self.get_absolute_url()
        coach = self.job_coach.username
        the_type = '<a target="_blank" href="' + url + '">' + self.get_type_display() + '</a>' if type_as_link else self.get_type_display()
        start = self.start_date.strftime(settings.DISPLAY_DATE) if self.start_date is not None else ''
        latest_status = self.get_latest_status()
        status = '' if latest_status is None else ' (' + latest_status.get_status_display() + ' )'
        end = (' to ' + self.end_date.strftime(settings.DISPLAY_DATE)) if self.end_date is not None else ''

        return the_type + ':' + coach + ' ' + start + end + status

    def get_full_type(self):
        return Contract.FULL_TYPES[self.type]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('contract_edit', args=[str(self.client.id), str(self.id)])

    def get_all_status_as_list(self):
        table = '<table >'
        for status in self.get_ordered_status():
            table = table + '<tr>' + '<td>'
            table = table + status.get_summary()
            table = table + '</td>' + '</tr>'
        table = table + '</table>'

        return table

    def get_derived_contract(self):
        con = self
        if (self.type == Contract.TIO):
            if con.__class__.__name__  == 'Contract':
                con = TIOContract.objects.get(pk=self.pk)

        return con

    def refresh_client_latest_contract(self):
        # make sure client is pointing to the latest contract
        # we maintain this relationship for performance gains
        latest_con = self.client.get_latest_contract_basic()
        self.client.latest_contract = latest_con
        self.client.save()

    def save(self, *args, **kwargs):
        super(Contract, self).save(*args, **kwargs)
        self.refresh_client_latest_contract(self)

    def delete(self, *args, **kwargs):
        super(Contract, self).save(*args, **kwargs)
        self.refresh_client_latest_contract(self)

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
    closed_date = models.DateField(null=True, blank=True)
    issue = models.IntegerField(choices=ISSUES, default=None, verbose_name='Adult 18+ with', null=True)
    consent_form_complete = models.BooleanField(default=False)
    aa_progress_jsa_18 = models.BooleanField(default=False, verbose_name='Progressing from Activity Agreements')
    add_support_jsa_18 = models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')
    add_support_jsa_25 = models.BooleanField(default=False, verbose_name='In need of additional support with health and personal confidence issues')
    wca_incapacity = models.BooleanField(default=False, verbose_name='Prior to WCA')
    support_esa = models.BooleanField(default=False, verbose_name='Support Group Category')
    wrag_esa = models.BooleanField(default=False, verbose_name='W.R.A.G (less than 3 months sustained employment in the last 3 yrs)')
    emp_pros_inc = models.BooleanField(default=False, verbose_name='To improve employment prospects')
    other_ben = models.TextField(verbose_name='Other Benefits', blank=True)
    fund_mgr_notes = models.TextField(verbose_name='Fund Manager Notes', blank=True)

    def get_info_man_acceptance_date(self):
        status = self.get_latest_status_with_state(ContractStatus.ACC_INFO_MAN)
        return status.created_on if status is not None else ''

    def get_fund_man_contact_date(self):
        return self.get_info_man_acceptance_date()

    def get_fund_man_approval_date(self):
        status = self.get_latest_status_with_state(ContractStatus.APP_FUND_MAN)

        return status.created_on if status is not None else ''

class ContractStatus(Auditable):
    AWAIT_INFO_MAN_ACC = 0
    ACC_INFO_MAN = 1
    APP_FUND_MAN = 2
    REJ_FUND_MAN = 3
    ACC_REV_INFO_MAN = 4
    AWAIT_FUND_APP_MAN = 5
    FUND_APP_MAN_UNDONE = 6
    STATUS = (
        (AWAIT_INFO_MAN_ACC, 'Awaiting info man acceptance'),
        (ACC_INFO_MAN, 'Accepted by info man'),
        (APP_FUND_MAN, 'Approved by fund man'),
        (REJ_FUND_MAN, 'Rejected by fund man'),
        (ACC_REV_INFO_MAN, 'Acceptance revoked by info man'),
        (AWAIT_FUND_APP_MAN, 'Awaiting fund manager approval'), # only iuse this for migrated tios, it will not be used after this
        (FUND_APP_MAN_UNDONE, 'Fund manager approval  undone'),
    )
    status = models.IntegerField(choices=STATUS, default=AWAIT_INFO_MAN_ACC)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, related_name="contract_status")

    def get_summary(self):
        return self.get_status_display() + ' - ' + self.modified_on.strftime(settings.DISPLAY_DATE_TIME)

    def __str__(self):
       return self.get_status_display() + ' - ' + str(self.contract)
