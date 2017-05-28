from client.models import Client, Contract, ContractStatus
import django_filters
from common.models import Address
from client.queries import *
from django.db.models import Max
from django.db.models import F

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class ClientFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    modified_on = django_filters.DateFilter(lookup_expr='gte')
    contract_type = django_filters.ChoiceFilter(choices=Contract.TYPES, method='filter_contract_type', name='contract_type', label='Contract type')
    contract_type_hist = django_filters.ChoiceFilter(choices=Contract.TYPES, method='filter_contract_type_hist', name='contract_type_hist', label='Contract type history')
    contract_status = django_filters.ChoiceFilter(choices=ContractStatus.STATUS, method='filter_contract_status', name='contract_status', label='Contract status history')
    modified_on = django_filters.DateFilter(label='Modified on >=')
    contract_started = django_filters.DateFilter(method='filter_contract_started', name='contract_started', label='Contract started >=')
    area = django_filters.ChoiceFilter(choices=Address.AREA, method='filter_address_area', name='filter_address_area', label='Area')
    age = django_filters.NumberFilter(method='filter_client_age', name='age', label='Age >=')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClientFilter, self).__init__(*args, **kwargs)
        # if I don't do this then out the box the initial queryset will be set to all Clients because I set
        # model to Client in the meta data below - so this is the starting querset before filter are applied
        self.queryset = get_client_search_default_queryset(user)
        # self.queryset = Client.objects.select_related('user').all()

    class Meta:
        model = Client
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['title', 'forename', 'surname', 'sex', 'modified_by', 'modified_on']

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_type(self, queryset, name, value):
        # see https://stackoverflow.com/questions/9838264/django-record-with-max-element
        # get the latest contract for each client and filter on type
        # TODO: suss if this is correct - see post I created: https://stackoverflow.com/questions/44229775/django-filterset-one-to-many-query
        #cons = Contract.objects.annotate(max_start_date=Max('start_date')).filter(start_date=F('max_start_date')).filter(type=value)
        # cons = Contract.objects.annotate(max_start_date=Max('start_date'))
        # print(cons.query)
        # results = queryset.annotate(max_start_date=Max('contract__start_date')).filter(contract__start_date=F('max_start_date')).filter(contract__type=value)
        # print(results.query)
        # return results
        return queryset

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_type_hist(self, queryset, name, value):
        return queryset.filter(**{'contract__type': value})

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_status(self, queryset, name, value):
        # return entries where any contracts have a status of value
        return queryset.filter(contract__contract_status__status=value).distinct()
        # return queryset.contract_set.all().order_by('start_date').first().contract_status.all().order_by('-modified_on').first(status=1)

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_started(self, queryset, name, value):
        return queryset.filter(**{'contract__start_date__gte': value})

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_address_area(self, queryset, name, value):
        return queryset.filter(**{'address__area': value})

    def filter_client_age(self, queryset, name, age):
        # https://stackoverflow.com/questions/23373151/filter-people-from-django-model-using-birth-date
        from datetime import date
        min_age = age
        max_date = date.today()
        try:
            max_date = max_date.replace(year=max_date.year - min_age)
        except ValueError:  # 29th of february and not a leap year
            assert max_date.month == 2 and max_date.day == 29
            max_date = max_date.replace(year=max_date.year - min_age, month=2, day=28)

        return queryset.filter(dob__lte=max_date)
