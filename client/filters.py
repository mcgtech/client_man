from client.models import Client
import django_filters

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['title', 'forename', 'surname', 'sex']