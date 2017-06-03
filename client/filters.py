from client.models import Client, Contract, ContractStatus
import django_filters
from common.models import Address
from common.filters import get_boolean_choices
from client.queries import *
from django.contrib.auth.models import User
from django.db.models import Max
from django.db.models import F
from django.conf import settings

# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
class ClientFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    contract_type = django_filters.ChoiceFilter(choices=Contract.TYPES, method='filter_contract_type', name='contract_type', label='Type')
    contract_status = django_filters.ChoiceFilter(choices=ContractStatus.STATUS, method='filter_contract_status', name='contract_status', label='Status')
    contract_started = django_filters.DateFilter(method='filter_contract_started', name='contract_started', label='Start date >=')
    contract_ended = django_filters.DateFilter(method='filter_contract_ended', name='contract_ended', label='End date <=')
    area = django_filters.ChoiceFilter(choices=Address.AREA, method='filter_address_area', name='filter_address_area', label='Area')
    # if I change the names of these then update the query names in tables.py
    age_from = django_filters.NumberFilter(method='filter_client_age_from', name='age_from', label='Age >=')
    age_to = django_filters.NumberFilter(method='filter_client_age_to', name='age_to', label='Age <=')
    live = django_filters.ChoiceFilter(choices=get_boolean_choices(), method='filter_on_live_contract', name='live', label='Live')
    all_coaches = User.objects.filter(groups__name=settings.JOB_COACH)
    coach_choices = []
    for coach in all_coaches:
        coach_choices.append((coach.id, coach.username))
    job_coach = django_filters.ChoiceFilter(choices=coach_choices, method='filter_job_coach', label='Job coach')

    LATEST_CON = 0
    ANY_CON = 1
    con_search_types = (
        (ANY_CON, 'Any contract'),
        (LATEST_CON, 'Latest contract'),
    )
    contract_search_targets = django_filters.ChoiceFilter(choices=con_search_types, method='filter_on_contract_search_targets',  name='contract_search_targets', label='Target')
    # modified_on = django_filters.DateFilter(lookup_expr='gte')
    # modified_on = django_filters.DateFilter(label='Modified on >=')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ClientFilter, self).__init__(*args, **kwargs)
        # if I don't do this then out the box the initial queryset will be set to all Clients because I set
        # model to Client in the meta data below - so this is the starting querset before filter are applied
        self.queryset = get_client_search_default_queryset(user)
        # self.queryset = Client.objects.select_related('user').all()

    # this does nothing, its only here so I can add a drop down whose value can be
    # ccessed in other filters as self.data['contract_search_targets']
    def filter_on_contract_search_targets(self, queryset, name, value):
        return queryset

    class Meta:
        model = Client
        # if I change this then also change: /Users/stephenmcgonigal/django_projs/client/templates/client/client/client_search.html
        fields = ['title', 'forename', 'surname', 'sex', 'live']

    def filter_on_live_contract(self, queryset, name, value):
        from datetime import date
        today = date.today()
        client_ids = []
        value = int(value)
        for client in queryset:
            latest_con = client.latest_contract
            is_live = latest_con is not None and (latest_con.end_date is None or latest_con.end_date >= today)
            if (is_live == True and value == 1) or (is_live == False and value == 0):
                client_ids.append(client.id)
        return queryset.filter(pk__in=client_ids)

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_job_coach(self, queryset, name, value):
        qs = queryset
        con_search_type = self.get_selected_contract_type()
        if con_search_type == self.LATEST_CON:
            qs = queryset.filter(**{'latest_contract__job_coach_id': value}).distinct()
        elif con_search_type == self.ANY_CON:
            # search all associated contracts
            qs = queryset.filter(**{'contract__job_coach_id': value}).distinct()

        return qs

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_status(self, queryset, name, value):
        qs = queryset
        con_search_type = self.get_selected_contract_type()
        if con_search_type == self.LATEST_CON:
            qs = queryset.filter(**{'latest_contract__contract_status__status': value}).distinct()
        elif con_search_type == self.ANY_CON:
            # search all associated contracts
            qs = queryset.filter(**{'contract__contract_status__status': value}).distinct()

        return qs

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_started(self, queryset, name, value):
        qs = queryset
        con_search_type = self.get_selected_contract_type()
        if con_search_type == self.LATEST_CON:
            qs = queryset.filter(**{'latest_contract__start_date__gte': value}).distinct()
        elif con_search_type == self.ANY_CON:
            # search all associated contracts
            qs = queryset.filter(**{'contract__start_date__gte': value}).distinct()

        return qs

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_ended(self, queryset, name, value):
        qs = queryset
        con_search_type = self.get_selected_contract_type()
        if con_search_type == self.LATEST_CON:
            qs = queryset.filter(**{'latest_contract__end_date__gte': value}).distinct()
        elif con_search_type == self.ANY_CON:
            # search all associated contracts
            qs = queryset.filter(**{'contract__end_date__gte': value}).distinct()

        return qs

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_address_area(self, queryset, name, value):
        return queryset.filter(**{'address__area': value})

    @staticmethod
    def get_date_for_age_searching(age):
        # https://stackoverflow.com/questions/23373151/filter-people-from-django-model-using-birth-date
        from datetime import date
        target_date = date.today()
        try:
            target_date = target_date.replace(year=target_date.year - age)
        except ValueError:  # 29th of february and not a leap year
            assert target_date.month == 2 and target_date.day == 29
            target_date = target_date.replace(year=target_date.year - age, month=2, day=28)

        return target_date

    def filter_client_age_from(self, queryset, name, age):
        max_date = self.get_date_for_age_searching(age)

        return queryset.filter(dob__lte=max_date)

    def filter_client_age_to(self, queryset, name, age):
        min_date = self.get_date_for_age_searching(age)

        return queryset.filter(dob__gte=min_date)


    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_contract_type(self, queryset, name, value):
        # I now store a link to latest contract in client
        # but I have left this code here for illustration purposes
        # see https://stackoverflow.com/questions/9838264/django-record-with-max-element
        # get the latest contract for each client and filter on type
        # my qn: https://stackoverflow.com/questions/44229775/django-filterset-one-to-many-query
        # for each client get the contract with the latest start date
        # if that contract has a type that matches the value parameter, then hold on to the pk of its parent
        # finally strip out any clients that are not in this list, from the queryset django-filter passed in and then return it
        # client_ids = []
        # value = int(value)
        # for client in queryset:
        #     con = Contract.objects.filter(client=client).order_by('start_date').last()
        #     if con is not None and con.type == value:
        #         client_ids.append(con.client.id)
        # return queryset.filter(pk__in=client_ids)
        qs = queryset
        con_search_type = self.get_selected_contract_type()
        if con_search_type == self.LATEST_CON:
            qs = queryset.filter(**{'latest_contract__type': value}).distinct()
        elif con_search_type == self.ANY_CON:
            # search all associated contracts
            qs = queryset.filter(**{'contract__type': value}).distinct()

        return qs

    def get_selected_contract_type(self):
        try:
            con_search_type = int(self.data['contract_search_targets'])
        except:
            con_search_type = self.ANY_CON

        return con_search_type
