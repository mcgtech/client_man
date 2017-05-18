from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Auditable(models.Model):
    created_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by', blank=True, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='modified_by', blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         self.created_on = timezone.now()
    #     else:
    #         self.created_on = self.created_on
    #     self.modified_on = timezone.now()
    #     super(Auditable, self).save(*args, **kwargs)

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

    # def save(self, *args, **kwargs):
    #     self.modified_date = timezone.now()
    #     super(Person, self).save(*args, **kwargs)

    def __str__(self):
       return self.TITLES[self.title] + ' ' + self.forename + ' ' + self.surname
    # @property
    # def age(self):
    #     today = date.today()
    #     return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
