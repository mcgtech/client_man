from django.db import models
from common.models import Auditable

class EmailTemplate(Auditable):
    CON_ACCEPT = 0
    CON_REVOKE = 1
    CON_APPROVE = 2
    CON_REJECT = 3
    CON_UNDO = 4
    TEMPLATE_NAMES = (
        (None, 'Please select'),
        (CON_ACCEPT, 'Contract accept'),
        (CON_REVOKE, 'Contract revoke'),
        (CON_APPROVE, 'Contract approve'),
        (CON_REJECT, 'Contract reject'),
        (CON_UNDO, 'Contract undo'),
    )
    template_identifier = models.IntegerField(choices=TEMPLATE_NAMES, default=None, unique=True)
    subject = models.CharField(max_length=100)
    from_address = models.CharField(max_length=100)
    to_addresses = models.TextField()
    cc_addresses = models.TextField(blank=True)
    bcc_addresses = models.TextField(blank=True)
    plain_body = models.TextField(help_text='This will be used if recipients software can not handle html')
    html_body = models.TextField(help_text='This will be used if recipients software can handle html')

    def __str__(self):
       return self.get_template_identifier_display()
