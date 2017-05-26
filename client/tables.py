from django.utils.html import format_html
from client.models import Client
from django_tables2 import tables, LinkColumn, A, SingleTableMixin, Column

class ClientsTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    client_id = LinkColumn('client_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})
    # https://stackoverflow.com/questions/26168985/django-tables-2-field-accessor-backward-relationship
    # I do this so that I can show the 1->m el between client and contracts using django-tables2
    # contracts = Column(accessor='contracts_data')

    # https://github.com/bradleyayers/django-tables2/issues/256
    # need orderable= False or it will break
    contracts = Column(empty_values=(), verbose_name='Contracts', orderable= False)
    # age is a calculatewed field, if I try to sort it django-tables2 will fail
    # so we do the following (see: http://django-tables2.readthedocs.io/en/latest/pages/ordering.html):
    age = Column(order_by=('dob'))

    def render_contracts(self, record):
        if record.contract.exists():
            con_links = [c.get_link() for c in record.contract.all().order_by('start_date')]
            return format_html("<br>".join(con_links), record)

    class Meta:
        model = Client
        # fiels to display in table
        fields = ('title', 'forename', 'surname', 'sex', 'job_coach', 'age', 'address.area')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('client_id', '...')