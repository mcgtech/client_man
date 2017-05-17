from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.contrib.auth.models import AbstractUser

# drop downs: http://stackoverflow.com/questions/31130706/dropdown-in-django-model
#             http://stackoverflow.com/questions/1117564/set-django-integerfield-by-choices-name
#class Person(models.Model):
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser
class Person(models.Model):
    CLIENT = 0
    JOB_COACH = 1
    MANAGER = 2
    PARTNER = 3
    TYPES = (
        (CLIENT, 'Client'),
        (JOB_COACH, 'Job Coach'),
        (MANAGER, 'Manager'),
        (PARTNER, 'Partner'),
    )
    MR = 0
    MRS = 1
    MISS = 2
    MS = 3
    TITLES = (
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MISS, 'Miss'),
        (MS, 'Ms'),
    )
    type = models.IntegerField(choices=TYPES, default=CLIENT)
    title = models.IntegerField(choices=TITLES, default=MR)
    middle_name = models.CharField(max_length=100, blank=True)
    known_as = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    forename = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    email_address = models.CharField(max_length=100, blank=True) # I use the validator in the form
    modified_date = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(User, blank=True, null=True)
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='Person')

    def save(self, *args, **kwargs):
        self.modified_date = timezone.now()
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
       return self.TITLES[self.title] + ' ' + self.forename + ' ' + self.surname
    # @property
    # def age(self):
    #     today = date.today()
    #     return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))


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
    WHITE_S = 13
    WHITE_W = 14
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
    sex = models.IntegerField(choices=SEX, default=MALE)
    marital_status = models.IntegerField(choices=MARITAL_STATUS, default=SINGLE)
    ethnicity = models.IntegerField(choices=ETHNICITY, default=WHITE_S)
    birth_certificate = models.FileField(upload_to='client/birth_certs/', blank=True, null=True)
    social_work_involved = models.BooleanField(default=False)


class Note(models.Model):
    note = models.TextField()
    modified_date = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(User, blank=True, null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, related_name="note")

    # def save(self, *args, **kwargs):
    #     self.modified_date = timezone.now()
    #     super(Note, self).save(*args, **kwargs)

    def __str__(self):
       return self.note


class Telephone(models.Model):
    HOME = 0
    WORK = 1
    MOBILE = 2
    PHONE_TYPES = (
        (HOME, 'Home'),
        (WORK, 'Work'),
        (MOBILE, 'Mobile'),
    )
    type = models.IntegerField(choices=PHONE_TYPES, default=MOBILE)
    number = models.CharField(max_length=100)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, related_name="Telephone")

    def get_type_for_display(self):
        return self.PHONE_TYPES[self.type]

    def __str__(self):
       return self.number + ' (' + self.get_type_for_display(self) + ')'

# see https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
# to see how I attach associate person with address
class Address(models.Model):
    line_1 = models.CharField(max_length=100, blank=True)
    line_2 = models.CharField(max_length=100, blank=True)
    line_3 = models.CharField(max_length=100, blank=True)
    post_code = models.CharField(max_length=100, blank=True)
    BAST = 0
    CAIT = 1
    INNA = 2
    LARB = 3
    ROSS = 4
    SKYE = 5
    SUTH = 6
    AREA = (
        (BAST, 'Badenoch and Strathspey'),
        (CAIT, 'Caithness'),
        (INNA, 'Inverness and Nairn'),
        (LARB, 'Lochaber'),
        (ROSS, 'Ross-shire'),
        (SKYE, 'Skye'),
        (SUTH, 'Sutherland'),
    )
    area = models.IntegerField(choices=AREA, default=BAST)
    evidence = models.FileField(upload_to='client/address_evidence/', blank=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, related_name="Address")

    def __str__(self):
       return self.line_1

    # def get_area_for_display(self):
    #     return self.AREA[self.area]
    #
    # def __str__(self):
    #    return self.line_1 + ' (' + self.get_area_for_display(self) + ')'