from common.views import *
from client.forms import *
from common.models import HTMLTemplate
from common.forms import HTMLTemplateForm
from django.shortcuts import get_object_or_404
import json

def show_report(request, entity_id, report_id):
    entity_id = int(entity_id)
    report_id = int(report_id)
    if report_id == 1:
        return show_client_report(request, entity_id)
    elif report_id == 2:
        return show_contract_report(request, entity_id)

@login_required
@user_passes_test(admin_user, 'job_coach_user')
def show_client_report(request, entity_id):
    client = get_object_or_404(Client, pk=entity_id)
    contracts = [c.get_summary(False) for c in client.get_all_contracts_ordered()]

    return render(request, 'client/client_details.html', {'client': client, 'contracts' : contracts})

@login_required
@user_passes_test(admin_user, 'client_man_login')
def show_contract_report(request, entity_id):
    x = 0