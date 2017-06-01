from .models import EmailTemplate
from django_tables2 import tables, LinkColumn, A

class EmailTempTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    id = LinkColumn('email_temp_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})

    class Meta:
        model = EmailTemplate
        # fields to display in table
        fields = ('id', 'template_identifier', 'subject', 'from_address', 'to_addresses', 'cc_addresses', 'bcc_addresses', 'plain_body', 'html_body')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('id', 'template_identifier', 'subject', 'from_address', 'to_addresses', 'cc_addresses', 'bcc_addresses', 'plain_body', 'html_body')