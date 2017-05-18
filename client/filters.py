from django.contrib.auth.models import User
import django_filters
from .models import Client

class ClientFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['forename', 'surname', ]
