from common.views import *
from client.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.template import Context, Template
from reporting.models import ReportTemplate
from django.http import HttpResponse

def show_report(request, entity_ids, report_id):
    report_id = int(report_id)
    entity_ids = entity_ids.split(",")
    if report_id == 1:
        return show_client_report(request, entity_ids)
    elif report_id == 2:
        return show_latest_contract_report(request, entity_ids)

@login_required
@user_passes_test(admin_user, 'job_coach_user')
def show_client_report(request, entity_ids):
    temp = ReportTemplate.objects.get(template_identifier=ReportTemplate.CLIENT_MAIN)
    if temp is not None:
        clients_markup = ''
        clients = Client.objects.filter(pk__in=entity_ids)
        pos = 1
        total = len(clients)
        for client in clients:
            latest_contract = client.get_latest_contract()
            context = {'client': client, 'latest_contract' : latest_contract}
            str_tpl = Template(temp.body)
            client_details = str_tpl.render(Context(context))
            clients_markup = clients_markup + client_details
            if total > 1 and pos != total:
                clients_markup = clients_markup + get_force_page_break_markup()
            pos = pos + 1

    return render(request, 'client/client_details_report.html', {'clients_markup': clients_markup})


@login_required
@user_passes_test(admin_user, 'client_man_login')
def show_latest_contract_report(request, entity_ids):
    clients_con_markup = ''
    clients = Client.objects.filter(pk__in=entity_ids)
    pos = 1
    total = len(clients)
    for client in clients:
        latest_contract = client.get_latest_contract()
        context = {'client': client, 'contract' : latest_contract}
        if latest_contract.type == Contract.TIO:
            temp = ReportTemplate.objects.get(template_identifier=ReportTemplate.CLIENT_LATE_TIO_CON)
        else:
            temp = ReportTemplate.objects.get(template_identifier=ReportTemplate.CLIENT_LATE_CON)
        str_tpl = Template(temp.body)
        con_details = str_tpl.render(Context(context))
        clients_con_markup = clients_con_markup + con_details
        if total > 1 and pos != total:
            clients_con_markup = clients_con_markup + get_force_page_break_markup()
        pos = pos + 1

    return render(request, 'client/client_contract_report.html', {'clients_con_markup': clients_con_markup})