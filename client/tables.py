from django.utils.html import format_html
from client.models import Client
from django_tables2 import tables, LinkColumn, A, CheckBoxColumn, Column
from django.utils.html import mark_safe

class ClientsTable(tables.Table):
    # selected = CheckBoxColumn(accessor="selected")
    selection = CheckBoxColumn(accessor='pk', orderable=False)

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
    # client.latest_contract.partner = Column(verbose_name='Partner', orderable= False)
    partner = Column(empty_values=(), verbose_name='Partner', orderable= False)

    def render_partner(self, record):
        return record.latest_contract.partner

    def render_contracts(self, record):
        if record.contract.exists():
            con_links = [c.get_summary(True) for c in record.get_all_contracts_ordered()]
            return format_html("<br>".join(con_links), record)


    class Meta:
        model = Client
        # fields to display in table
        fields = ('title', 'forename', 'surname', 'sex', 'age', 'address.area', 'original_client_id')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('selection', 'client_id', 'title', 'forename', 'surname', 'sex', 'age', 'address.area', 'partner', 'contracts', 'original_client_id')