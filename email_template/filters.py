import django_filters
from .models import EmailTemplate
from client.queries import *

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class EmailTempFilter(django_filters.FilterSet):
    template_identifier = django_filters.ChoiceFilter(choices=EmailTemplate.TEMPLATE_NAMES, label='Template')

    class Meta:
        model = EmailTemplate
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['template_identifier']
