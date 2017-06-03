from django.utils.html import format_html
from client.models import Client
from django_tables2 import tables, LinkColumn, A, CheckBoxColumn, Column
from django.utils.html import mark_safe
from crequest.middleware import CrequestMiddleware
import dateutil.parser
import time
from django.conf import settings

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
    # age is a calculated field, if I try to sort it django-tables2 will fail
    # so we do the following (see: http://django-tables2.readthedocs.io/en/latest/pages/ordering.html):
    age = Column(order_by=('dob'), verbose_name='Current age')
    # client.latest_contract.partner = Column(verbose_name='Partner', orderable= False)
    partner = Column(empty_values=(), verbose_name='Partner', orderable= False)
    age_at_time = Column(empty_values=(), verbose_name='Age during search period', orderable= False)

    def render_age_at_time(self, record):
        current_request = CrequestMiddleware.get_request()
        contract_started = self.get_query_by_key('contract_started')
        contract_ended = self.get_query_by_key('contract_ended')
        # contract_started = dateutil.parser.parse(contract_started);
        # print(str(contract_started))
        if contract_started is not None and contract_ended is not None:
            contract_started = time.strptime(contract_started, settings.DISPLAY_DATE)
            contract_started = dateutil.parser.parse(time.strftime("%Y-%m-%d", contract_started));
            contract_ended = time.strptime(contract_ended, settings.DISPLAY_DATE)
            contract_ended = dateutil.parser.parse(time.strftime("%Y-%m-%d", contract_ended));
            diff = contract_ended - contract_started
            print(diff)
        # print(time.strftime("%d/%m/%Y",conv))
        period_age = 12
        return period_age

    def render_partner(self, record):
        return record.latest_contract.partner if record.latest_contract is not None else None

    def render_contracts(self, record):
        if record.contract.exists():
            con_links = [c.get_summary(True) for c in record.get_all_contracts()]
            return format_html("<br>".join(con_links), record)

    def get_query_by_key(self, key):
        value = None
        if self.request.GET is not None and key in self.request.GET:
            value = self.request.GET[key]
        return value

    def __init__(self, *args, **kwargs):
        super(ClientsTable, self).__init__(*args, **kwargs)
        # to get current request objct: https://stackoverflow.com/questions/30424056/django-tables2-use-request-user-in-render-method
        self.request = CrequestMiddleware.get_request()

    class Meta:
        model = Client
        # fields to display in table
        fields = ('title', 'forename', 'surname', 'sex', 'age', 'address.area', 'original_client_id')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('selection', 'client_id', 'title', 'forename', 'surname', 'sex', 'age', 'address.area', 'partner', 'contracts', 'original_client_id')