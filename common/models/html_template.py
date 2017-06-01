from django.db import models
from common.models import Auditable

class HTMLTemplate(Auditable):
    CON_ACCEPT = 0
    CON_REVOKE = 1
    CON_APPROVE = 2
    CON_REJECT = 3
    TEMPLATE_NAMES = (
        (None, 'Please select'),
        (CON_ACCEPT, 'Contract accept'),
        (CON_REVOKE, 'Contract revoke'),
        (CON_APPROVE, 'Contract approve'),
        (CON_REJECT, 'Contract reject'),
    )
    EMAIL_TEMP_TYPE = 0
    REPORT_TEMP_TYPE = 1
    TEMPLATE_TYPES = (
        (None, 'Please select'),
        (EMAIL_TEMP_TYPE, 'Email'),
        (REPORT_TEMP_TYPE, 'Report'),
    )
    template_identifier = models.IntegerField(choices=TEMPLATE_NAMES, default=None)
    type = models.IntegerField(choices=TEMPLATE_TYPES, default=None)
    body = models.TextField()

    def __str__(self):
       return self.get_template_identifier_display()
