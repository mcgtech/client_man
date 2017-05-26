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
        end = (' to ' + self.end_date.strftime(settings.DISPLAY_DATE)) if self.end_date is not None else ''

        return link + ' ' + start + end

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('contract_edit', args=[str(self.client.id), str(self.id)])

    def __str__(self):
       return '' if self.client is None else self.client.get_full_name() + ' - '+ self.get_type_display() + ' - ' + self.start_date.strftime(settings.DISPLAY_DATE)
