from client.models import Client
from common.models import Person, Note, Address, Telephone
from common.views import form_errors_as_array, super_user_or_job_coach, super_user_or_admin, show_form_error
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.http import HttpResponse
import json

# code in view which returns json data
# http://www.lalicode.com/post/5/
@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def quick_client_search(request):
  if request.is_ajax():
    term = request.GET.get('term', '')
    if term:
        if term.isdigit():
            # TODO: hunt down Client.objects.select_related('user') and put into a function
            clients = Client.objects.select_related('user').filter(pk = term)
        else:
            clients = Person.find_person_by_full_name(term)
    else:
        clients = Client.objects.all()
    results = []
    # TODO: add name of coach at end od full name (do this inside the Client model class)
    for client in clients:
        client_json = {}
        client_json['id'] = client.id
        client_json['label'] = client.get_full_name()
        client_json['value'] = client.get_full_name()
        results.append(client_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'

  return HttpResponse(data, mimetype)


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_search(request):
    # this is simply getting all clients and then filtering client side using the js helper: https://www.datatables.net/
    # if this becomes a perf problem then read: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
    # note however that https://www.datatables.net/ can use ajax to reduce no of client returned, if I go down this pass then consider
    # using https://github.com/shymonk/django-datatable
    #
    # https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html
	clients = Client.objects.select_related('user').all()
	return render(request, 'search/client_search.html', {'clients' : clients})
