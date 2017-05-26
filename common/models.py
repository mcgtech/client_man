from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in

class Auditable(models.Model):
    created_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_created_by', blank=True, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modified_by', blank=True, null=True)

    class Meta:
        abstract = True


# drop downs: http://stackoverflow.com/questions/31130706/dropdown-in-django-model
#             http://stackoverflow.com/questions/1117564/set-django-integerfield-by-choices-name
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser
# class Person(Auditable):
class Person(Auditable):
    MR = 0
    MRS = 1
    MISS = 2
    MS = 3
    TITLES = (
        (None, 'Please select'),
        (MR, 'Mr'),
        (MRS, 'Mrs'),
        (MISS, 'Miss'),
        (MS, 'Ms'),
    )
    title = models.IntegerField(choices=TITLES, default=None)
    middle_name = models.CharField(max_length=100, blank=True)
    known_as = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    forename = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    email_address = models.CharField(max_length=100, blank=True) # I use the validator in the form
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='person')

    def get_full_name(self):
        return self.get_title_display() + ' ' + self.forename + ' ' + self.surname

    def __str__(self):
       return self.get_full_name()

    # decorator to make it look like a normal attribute.
    @property
    def age(self):
        client_age = 0
        if self.dob is not None:
            today = date.today()
            client_age =  today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

        return client_age


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
    MOBILE = 1
    PARENTS = 2
    WORK = 3
    PHONE_TYPES = (
        (None, 'Please select'),
        (HOME, 'Home'),
        (MOBILE, 'Mobile'),
        (PARENTS, 'Parents'),
        (WORK, 'Work'),
    )
    type = models.IntegerField(choices=PHONE_TYPES, default=None)
    number = models.CharField(max_length=100, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, related_name="telephone")

    # def get_type_for_display(self):
    #     return self.PHONE_TYPES[self.type]

    def __str__(self):
       return self.number
       # return self.number + ' (' + self.get_type_display(self) + ')'


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
        (None, 'Please select'),
        (BAST, 'Badenoch and Strathspey'),
        (CAIT, 'Caithness'),
        (INNA, 'Inverness and Nairn'),
        (LARB, 'Lochaber'),
        (ROSS, 'Ross-shire'),
        (SKYE, 'Skye'),
        (SUTH, 'Sutherland'),
    )
    area = models.IntegerField(choices=AREA, default=None)
    evidence = models.FileField(upload_to='client/address_evidence/', blank=True)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, null=True, related_name="address")

    def __str__(self):
       return self.line_1 + ', ' + self.line_2 + ', ' + self.get_area_display()
