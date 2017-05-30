from django.db import models
from django.contrib.auth.models import User
from .person import Person

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
