from django.db import models
from django.conf import settings
from datetime import date
from .auditable import Auditable
from django.contrib.auth.models import User

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

    def __str__(self):
        add = []
        if len(self.line_1.strip()):
            add.append(self.line_1.strip())
        if len(self.line_2.strip()):
            add.append(self.line_2.strip())
        if len(self.line_3.strip()):
            add.append(self.line_3.strip())
        add.append(self.get_area_display())

        return ", ".join(add)


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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='person')
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, related_name="person")

    def get_telephone_display(self):
        telephones = []
        for tele in self.telephone.all():
            telephones.append(str(tele))
        return ", ".join(telephones)

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

    def __str__(self):
       return self.number + ' (' + self.get_type_display() + ')'

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
