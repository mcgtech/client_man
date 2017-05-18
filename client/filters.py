from django.contrib.auth.models import User
import django_filters
from .models import Client

class ClientFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')
    middle_name = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    year_of_birth = django_filters.NumberFilter(name='dob', lookup_expr='year')
    class Meta:
        model = Client
        fields = ['forename', 'surname']
