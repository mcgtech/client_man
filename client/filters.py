from client.models import Client, Contract
import django_filters

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class ClientFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    contract_type = django_filters.ChoiceFilter(choices=Contract.TYPES, method='filter_contract_type', name='contract_type', label='Contract type')

    def __init__(self, *args, **kwargs):
        super(ClientFilter, self).__init__(*args, **kwargs)
        # if I don't do this then out the box the initial queryset will be set to all Clients because I set
        # model to Client in the meta data below - so this is the starting querset before filter are applied
        # self.queryset = Client.objects.select_related('user').all().filter(surname__startswith='Aitken')

    class Meta:
        model = Client
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['title', 'forename', 'surname', 'sex', 'modified_by',]

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_type(self, queryset, name, value):
        return queryset.filter(**{'contract__type': value})