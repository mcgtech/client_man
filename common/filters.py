import django_filters
from common.models import HTMLTemplate
from client.queries import *

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class HTMLTempFilter(django_filters.FilterSet):
    template_identifier = django_filters.ChoiceFilter(choices=HTMLTemplate.TEMPLATE_NAMES, label='Template')
    type = django_filters.ChoiceFilter(choices=HTMLTemplate.TEMPLATE_TYPES, label='Type')

    class Meta:
        model = Client
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['template_identifier', 'type']
