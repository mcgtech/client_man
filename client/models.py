from django.db import models
from common.models import Person, Auditable
from django.conf import settings

class Client(Person):
    MALE = 0
    FEMALE = 1
    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    DIVORCED = 0
    MARRIED = 1
    SEPARATED = 2
    SINGLE = 3
    TBC = 4
    TO_BE_ASS = 5
    WIDOWED = 6
    MARITAL_STATUS = (
        (DIVORCED, 'Divorced'),
        (MARRIED, 'Married'),
        (SEPARATED, 'Separated'),
        (SINGLE, 'Single'),
        (TBC, 'TBC'),
        (TO_BE_ASS, 'To Be Assigned'),
        (WIDOWED, 'Widowed'),
    )
    ASIAN_B = 0
    ASIAN_C = 1
    ASIAN_I = 2
    ASIAN_O = 3
    ASIAN_P = 4
    BLACK_A = 5
    BLACK_C = 6
    BLACK_O = 7
    MIXED = 8
    OTHER = 9
    TBC = 10
    TRAVEL = 11
    WHITE_E = 12
    WHITE_I = 13
    WHITE_O = 14
    WHITE_S = 15
    WHITE_W = 16
    ETHNICITY = (
        (ASIAN_B, 'Asian (Bangladesh)'),
        (ASIAN_C, 'Asian (Chinese)'),
        (ASIAN_I, 'Asian (Indian)'),
        (ASIAN_O, 'Asian (Other)'),
        (ASIAN_P, 'Asian (Pakistan)'),
        (BLACK_A, 'Black (African)'),
        (BLACK_C, 'Black (Caribbean)'),
        (BLACK_O, 'Black (Other)'),
        (MIXED, 'Mixed Background'),
        (OTHER, 'Other Ethinicity'),
        (TBC, 'TBC'),
        (TRAVEL, 'Traveller/Gypsy'),
        (WHITE_E, 'White (English)'),
        (WHITE_I, 'White (Irish)'),
        (WHITE_O, 'White (Other)'),
        (WHITE_S, 'White (Scottish)'),
        (WHITE_W, 'White (Welsh)'),
    )
    NO_QUAL = 0
    ACCESS_1_2 = 1
    ACCESS_3 = 2
    GENERAL = 3
    CREDIT = 4
    STANDARD = 5
    HIGHER = 6
    HNC = 7
    HND = 8
    EDUCATION = (
        (None, 'Please select'),
        (NO_QUAL, 'No qualifications'),
        (ACCESS_1_2, 'Access 1 or 2'),
        (ACCESS_3, 'Access 3 or foundation standard grade'),
        (GENERAL, 'General standard grade or intermediate 1'),
        (CREDIT, 'Credit'),
        (STANDARD, 'Standard grade or intermediate 2'),
        (HIGHER, 'Higher'),
        (HNC, 'HNC or advanced Higher'),
        (HND, 'HND or Degree'),
    )
    BUS_GATE = 0
    COLLEGE = 1
    HI_COU = 2
    JOB_CENT = 3
    NESS = 4
    NHS = 5
    RAG_TAG = 6
    RE_REG = 7
    SCHOOL = 8
    SHIRLIE = 9
    SDS = 10
    SOC_WORK = 11
    WORD = 12
    REC_BY = (
        (None, 'Please select'),
        (BUS_GATE, 'Business Gateway'),
        (COLLEGE, 'College'),
        (HI_COU, 'Highland Council Employability team'),
        (JOB_CENT, 'Jobcentre Plus'),
        (NESS, 'Ness Toiletries'),
        (NHS, 'NHS'),
        (RAG_TAG, 'Rag Tag N Textile'),
        (RE_REG, 'Re-registration'),
        (SCHOOL, 'School'),
        (SHIRLIE, 'Shirlie Project'),
        (SDS, 'Skills Development Scotland'),
        (SOC_WORK, 'Social Work'),
        (WORD, 'Word of mouth (friend/family)'),
    )
    NO = 0
    YES = 1
    MAND_BOOL = (
        (None, 'Please select'),
        (NO, 'No'),
        (YES, 'Yes'),
    )
    INACTIVE = 0
    EMPLOYED = 1
    LONG_EMPLOYED = 2
    NEET = 3
    UNEMPLOYED = 4
    EMPLOY_STATES = (
        (None, 'Please select'),
        (INACTIVE, 'Economically Inactive'),
        (EMPLOYED, 'Employed (including self-employed)'),
        (LONG_EMPLOYED, 'Long Term Employed'),
        (NEET, 'NEET Inactive'),
        (UNEMPLOYED, 'Unemployed'),
    )
    STAGE_2 = 0
    STAGE_3 = 1
    LONG_EMPLOYED = 2
    EIGHTEEN_PLUS = 3
    STAGES = (
        (None, 'Please select'),
        (STAGE_2, 'Stage 2'),
        (STAGE_3, 'Stage 3'),
        (EIGHTEEN_PLUS, '18+'),
    )
    MON_6 = 0
    MON_6_12 = 1
    MON_12_24 = 2
    MON_25_36 = 3
    OVER_3 = 4
    TBC = 5
    ATT_SCHOOL = 6
    TIME_UNEMP = (
        (None, 'Please select'),
        (MON_6, 'Up to 6 months'),
        (MON_6_12, '6 - 12 months'),
        (MON_12_24, '13 - 24 months'),
        (MON_25_36, '25 - 36 months'),
        (OVER_3, 'Over 3 years'),
        (TBC, 'TBC'),
        (ATT_SCHOOL, 'Attending School'),
    )
    AUTISM = 0
    DYSPRAXIA = 1
    HEAD_IN = 2
    LEARN_DIFF = 3
    LOW_SKILL = 4
    MENT_HEALTH = 5
    NO_EXP = 6
    TBA = 7
    UNEMP = 8
    YP_NEET = 9
    CLIENT_GROUPS = (
        (None, 'Please select'),
        (AUTISM, 'Autism'),
        (DYSPRAXIA, 'Dyspraxia'),
        (HEAD_IN, 'Head Injury'),
        (LEARN_DIFF, 'Learning Difficulties'),
        (LOW_SKILL, 'Low Skilled'),
        (MENT_HEALTH, 'Mental Health'),
        (NO_EXP, 'No Experience of Work'),
        (TBA, 'To Be Assigned'),
        (UNEMP, 'Unemployed (Under 3yrs no health issue)'),
        (YP_NEET, 'Young People (NEET)'),
    )
    client_group = models.IntegerField(choices=CLIENT_GROUPS, default=None)
    client_group_evidence = models.FileField(upload_to='client/group_evid/', blank=True, null=True)
    time_unemployed = models.IntegerField(choices=TIME_UNEMP, default=None)
    stage = models.IntegerField(choices=STAGES, default=None, null=True)
    employment_status = models.IntegerField(choices=EMPLOY_STATES, default=None)
    employment_status_evidence = models.FileField(upload_to='client/emp_state_evid/', blank=True, null=True)
    jsa = models.IntegerField(choices=MAND_BOOL, default=None)
    recommended_by = models.IntegerField(choices=REC_BY, default=None)
    education = models.IntegerField(choices=EDUCATION, default=None)
    sex = models.IntegerField(choices=SEX, default=MALE)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, default=SINGLE)
    ethnicity = models.IntegerField(choices=ETHNICITY, default=WHITE_S)
    birth_certificate = models.FileField(upload_to='client/birth_certs/', blank=True, null=True)
    social_work_involved = models.BooleanField(default=False)
    ref_received = models.BooleanField(default=False)
    # id on old system - set during migration - can be deleted once migration is complete
    original_client_id = models.IntegerField(default=0)
    nat_ins_number = models.CharField(max_length=100, blank=True)
    job_coach = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='job_coach', blank=True, null=True, limit_choices_to={'groups__name': "job coach"})
    end_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('client_edit', args=[str(self.id)])


class Contract(Auditable):
    AA = 0
    BP = 1
    EF = 2
    MIR = 3
    PP = 4
    TIO = 5
    WP = 6
    TYPES = (
        (None, 'Please select'),
        (AA, 'Activity Agreement'),
        (BP, 'Big Picture'),
        (EF, 'Employability Fund'),
        (MIR, 'MIR'),
        (PP, 'PP'),
        (TIO, 'TIO'),
        (WP, 'Work Programme'),
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
    YP_IN_CARE = 20
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
        (YP_IN_CARE, 'Young People Leaving Care'),
    )
    type = models.IntegerField(choices=TYPES, default=None)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    referral_date = models.DateField(null=True, blank=True)
    secondary_client_group = models.IntegerField(choices=SEC_CLIENT_GROUPS, default=None)
    secondary_client_group_evidence = models.FileField(upload_to='client/group_evid/', blank=True, null=True)
    application_form = models.FileField(upload_to='client/con_app_form/', blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, related_name="contract")

