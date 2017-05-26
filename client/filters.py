from client.models import Client, Contract
import django_filters
from common.models import Address
from client.queries import *

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class ClientFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    modified_on = django_filters.DateFilter(lookup_expr='gte')
    contract_type = django_filters.ChoiceFilter(choices=Contract.TYPES, method='filter_contract_type', name='contract_type', label='Contract type')
    contract_started = django_filters.DateFilter(method='filter_contract_started', name='contract_started', label='Contract started is greater than or equal to:')
    area = django_filters.ChoiceFilter(choices=Address.AREA, method='filter_address_area', name='filter_address_area', label='Area')
    # age = django_filters.NumberFilter(method='filter_client_age', name='age', label='Age')

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
        return queryset.filter(**{'contract__type': value})

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_started(self, queryset, name, value):
        return queryset.filter(**{'contract__start_date__gte': value})

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_address_area(self, queryset, name, value):
        return queryset.filter(**{'address__area': value})

    # def filter_client_age(self, queryset, name, age):
    #     return queryset.filter()
