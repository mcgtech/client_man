from client.models import Client
from common.models import Person, Note, Address, Telephone
from common.views import form_errors_as_array, job_coach_user, job_coach_man_user, admin_user, show_form_error
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
import json
from client.filters import ClientFilter
from client.queries import *
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin
from client.tables import ClientsTable
from django_tables2 import SingleTableView

# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class ClientViewFilter(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = u"job coach"
    model = Client
    table_class = ClientsTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = ClientFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='client/client/client_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 15}
    context_table_name = 'clients_table'

    # pass arguments into ClientFilter: https://stackoverflow.com/questions/37135320/django-pass-extra-arguments-to-filterset-class
    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(ClientViewFilter, self).get_filterset_kwargs(filterset_class)
        request = kwargs['request'];
        kwargs['user'] = request.user
        return kwargs


# I have kept the following just in case I need it later
# it search and then uses dttatable.js to apply filtering and pagination
@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def client_search_old(request):
    # this is simply getting all clients and then filtering client side using the js helper: https://www.datatables.net/
    # if this becomes a perf problem then read: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
    # note however that https://www.datatables.net/ can use ajax to reduce no of client returned, if I go down this pass then consider
    # using https://github.com/shymonk/django-datatable
    #
    # https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html
	clients = get_client_search_default_queryset(request.user)
	return render(request, 'search/client_search_old.html', {'clients' : clients})


# code in view which returns json data
# http://www.lalicode.com/post/5/
@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def quick_client_search(request):
  if request.is_ajax():
    term = request.GET.get('term', '')
    if term:
        if term.isdigit():
            # TODO: hunt down Client.objects.select_related('user') and put into a function#
            clients = get_client_search_default_queryset(request.user).filter(pk = term)
        else:
            clients = find_client_by_full_name(term, request.user)
    else:
        clients = get_client_search_default_queryset(request.user)
    results = []
    # TODO: add name of coach at end od full name (do this inside the Client model class)
    for client in clients:
        client_json = {}
        client_json['id'] = client.id
        client_json['label'] = client.get_full_name() + ' (' + client.job_coach.username + ')'
        client_json['value'] = client.get_full_name()
        results.append(client_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'

  return HttpResponse(data, mimetype)
