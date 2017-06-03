from django.utils.html import format_html
from client.models import Client
from django_tables2 import tables, LinkColumn, A, CheckBoxColumn, Column
from django.utils.html import mark_safe
from crequest.middleware import CrequestMiddleware
import dateutil.parser
import time
from common.models import Person
from django.conf import settings
from common.views import get_query_by_key

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
    age_at_time = Column(empty_values=(), verbose_name='Age (period)', orderable= False)

    def render_age_at_time(self, record):
        period_age = 'N/A'
        contract_started = get_query_by_key(self.request,'contract_started')
        contract_ended = get_query_by_key(self.request, 'contract_ended')
        if contract_started is not None and contract_ended is not None and len(contract_started) > 0 and len(contract_ended) > 0:
            # first we convert the uk date into time object and then create dateutil by converting the time
            # obj into iso date
            contract_started = time.strptime(contract_started, settings.DISPLAY_DATE)
            contract_started = dateutil.parser.parse(time.strftime("%Y-%m-%d", contract_started));
            contract_ended = time.strptime(contract_ended, settings.DISPLAY_DATE)
            contract_ended = dateutil.parser.parse(time.strftime("%Y-%m-%d", contract_ended));
            diff = contract_ended - contract_started
            diff = int(diff.days)
            if diff <= 365:
                start_period_age = Person.age_at_point_in_time(record.dob, contract_started)
                end_period_age = Person.age_at_point_in_time(record.dob, contract_started)
                if (start_period_age == end_period_age):
                    period_age = start_period_age
                else:
                    period_age = str(start_period_age) + ' (' + str(end_period_age) + ')'
        return period_age

    def render_partner(self, record):
        return record.latest_contract.partner if record.latest_contract is not None else None

    def render_contracts(self, record):
        if record.contract.exists():
            con_links = [c.get_summary(True) for c in record.get_all_contracts()]
            return format_html("<br>".join(con_links), record)

    def __init__(self, *args, **kwargs):
        super(ClientsTable, self).__init__(*args, **kwargs)
        # to get current request objct: https://stackoverflow.com/questions/30424056/django-tables2-use-request-user-in-render-method
        self.request = CrequestMiddleware.get_request()

    class Meta:
        model = Client
        # fields to display in table
        fields = ('title', 'forename', 'surname', 'sex', 'age', 'address.area', 'original_client_id')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('selection', 'client_id', 'title', 'forename', 'surname', 'sex', 'age', 'age_at_time', 'address.area', 'partner', 'contracts', 'original_client_id')