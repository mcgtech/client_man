from client.models import Client
import django_filters

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['forename', 'surname', 'sex']