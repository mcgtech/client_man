from django.db import models
from common.models import Auditable

class ReportTemplate(Auditable):
    CLIENT_MAIN = 0
    CLIENT_LATE_CON = 1
    CLIENT_LATE_TIO_CON = 2
    TEMPLATE_NAMES = (
        (None, 'Please select'),
        (CLIENT_MAIN, 'Client main details'),
        (CLIENT_LATE_CON, 'Latest client contract'),
        (CLIENT_LATE_TIO_CON, 'Latest client TIO contract'),
    )
    template_identifier = models.IntegerField(choices=TEMPLATE_NAMES, default=None, unique=True)
    body = models.TextField()

    def __str__(self):
       return self.get_template_identifier_display()
