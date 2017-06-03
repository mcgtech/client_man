from client.models import Client
from common.models import Person, Note, Address, Telephone
from common.views import form_errors_as_array, job_coach_user, job_coach_man_user, admin_user, show_form_error, get_query_by_key
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.conf import settings
from client.filters import ClientFilter
from client.queries import *
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin
from client.tables import ClientsTable
from django_tables2 import SingleTableView
import csv

# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class ClientViewFilter(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = [settings.JOB_COACH, settings.HI_COUNCIL_PART, settings.RAG_TAG_PART]
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

    # https://www.imagescape.com/blog/2016/03/03/django-class-based-views-basics/
    # def render_to_response(self, context, **reponse_kwargs):

    # renders template response rendered with passed in context
    # so I need to access table stuff
    # https://www.imagescape.com/blog/2016/03/03/django-class-based-views-basics/
    def get_context_data(self, **kwargs):
        # the context is passed into the template
        context = super(ClientViewFilter, self).get_context_data(**kwargs)

        # TODO: only do this when they have selected download
        # setup csv file for download
        # https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        filtered_queries = context['object_list'] # with no pagination
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['Id', 'First name', 'Last name', 'Date of birth', 'Job Coach'])
        # TODO: what is there is no contract - will job coach cause it to fail?
        clients = filtered_queries.values_list('id', 'forename', 'surname', 'dob', 'latest_contract__job_coach')
        for client in clients:
            writer.writerow(client)
        context['csv_response'] = response

        return context

    def get(self, request, *args, **kwargs):
        # the line between ---> and <---- were taken from cmenv/lib/python3.5/site-packages/django_filters/views.py
        # --->
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        self.object_list = self.filterset.qs
        context = self.get_context_data(filter=self.filterset,
                                        object_list=self.object_list)
        # <----
        csv_reqd = get_query_by_key(request, 'csv_reqd')
        if csv_reqd is not None:
            return context['csv_response']
        else:
            return self.render_to_response(context)



# code in view which returns json data
# http://www.lalicode.com/post/5/
@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def quick_client_search(request):
  if request.is_ajax():
    term = request.GET.get('term', '')
    if term:
        if term.isdigit():
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
        post_code = str(client.address.post_code)
        client_json['label'] = client.get_full_name() + ' (' + post_code + ')'
        client_json['value'] = client.get_full_name()
        results.append(client_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'

  return HttpResponse(data, mimetype)


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