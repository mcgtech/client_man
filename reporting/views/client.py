from common.views import *
from client.forms import *
from common.models import HTMLTemplate
from common.forms import HTMLTemplateForm
from django.shortcuts import get_object_or_404
import json

def show_report(request, entity_ids, report_id):
    report_id = int(report_id)
    entity_ids = entity_ids.split(",")
    if report_id == 1:
        return show_client_report(request, entity_ids)
    elif report_id == 2:
        return show_contract_report(request, entity_ids)

@login_required
@user_passes_test(admin_user, 'job_coach_user')
def show_client_report(request, entity_ids):
    clients = Client.objects.filter(pk__in=entity_ids)

    return render(request, 'client/client_details_report.html', {'clients': clients})

@login_required
@user_passes_test(admin_user, 'client_man_login')
def show_contract_report(request, entity_id):
    x = 0