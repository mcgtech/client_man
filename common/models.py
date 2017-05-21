from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import date
from django.db.models import Q

class Auditable(models.Model):
    created_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by', blank=True, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_by', blank=True, null=True)

    class Meta:
        abstract = True


# drop downs: http://stackoverflow.com/questions/31130706/dropdown-in-django-model
#             http://stackoverflow.com/questions/1117564/set-django-integerfield-by-choices-name
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser
# class Person(Auditable):
class Person(Auditable):
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
    # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='Person')

    def get_full_name(self):
        return self.get_title_display() + ' ' + self.forename + ' ' + self.surname

    def __str__(self):
       return self.get_full_name()

    @property
    def age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    def find_person_by_full_name(query_name):
       qs = Person.objects.select_related('user').all()
       for term in query_name.split():
         qs = qs.filter( Q(forename__icontains = term) | Q(middle_name__icontains = term) | Q(surname__icontains = term))

       return qs


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
        (HOME, 'Home'),
        (MOBILE, 'Mobile'),
        (PARENTS, 'Parents'),
        (WORK, 'Work'),
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
