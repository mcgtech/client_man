from django.conf import settings
from common.views import msg_once_only
from reporting.models import ReportTemplate
from django.template import Context, Template
import json
from braces.views import GroupRequiredMixin
from reporting.filters import ReportTempFilter
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from constance import config

from client.forms import *
from common.views import *
from reporting.tables import ReportTempTable
from reporting.forms import ReportTemplateForm


# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class ReportTempSearch(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = u"job coach"
    model = ReportTemplate
    table_class = ReportTempTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = ReportTempFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='report_template_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 15}
    context_table_name = 'report_temp_table'


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def report_temp_new(request):
    return manage_report_temp(request, None)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def report_temp_edit(request, pk):
    return manage_report_temp(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_report_temp(request, temp_id=None):
    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (accessed via data_from_django in js)
    js_dict = {}
    if temp_id is None:
        temp = ReportTemplate()
        the_action_text = 'Create'
        is_edit_form = False
        action = '/report_temp/new/'
        msg_once_only(request, 'Adding a new report template', settings.WARN_MSG_TYPE)
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        temp = get_object_or_404(ReportTemplate, pk=temp_id)
        action = '/report_temp/' + str(temp_id) + '/edit' + '/'

    if request.method == "POST":
        if request.POST.get("delete-record"):
            msg_once_only(request, 'You have successfully deleted the report template ' + str(temp), settings.INFO_MSG_TYPE)
            temp.delete()
            return redirect('/report_temp_search')
        temp_form = ReportTemplateForm(request.POST, request.FILES, instance=temp, prefix="main", is_edit_form=is_edit_form, cancel_url=None)
        if temp_form.is_valid():
            temp = temp_form.save(commit=False)
            apply_auditable_info(temp, request)
            temp.save()
            action = '/report_temp/' + str(temp.id) + '/edit' + '/'
            msg_once_only(request, 'Saved email template ' + str(temp), settings.INFO_MSG_TYPE)
            return redirect(action)
    else:
        cancel_url = redirect('report_temp_search').url
        temp_form = ReportTemplateForm(instance=temp, prefix="main", is_edit_form=is_edit_form, cancel_url=cancel_url)

    set_deletion_status_in_js_data(js_dict, request.user, admin_user)
    js_data = json.dumps(js_dict)

    temp_form_errors = form_errors_as_array(temp_form)

    return render(request, 'report_template.html', {'form': temp_form,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form,
                                                       'the_action': action, 'js_data' : js_data,
                                                       'form_errors': temp_form_errors,
                                                        'client_reflections' : get_client_reflections()})

def send_Report_using_template(context, template_id, request, test_to_addresses = None):
    if template_id is not None:
        temp = ReportTemplate.objects.get(template_identifier=template_id)
        if temp is not None:
            apply_agency_details_to_context(context)
            # run body through template to replace template variables - ie the stuff inside {{ }}
            html_content = apply_context_to_string(temp.html_body, context)
            plain_content = apply_context_to_string(temp.plain_body, context)
            subject = apply_context_to_string(temp.subject, context)
            from_Report = apply_context_to_string(temp.from_address, context)
            to_addresses = test_to_addresses if not None else temp.to_addresses
            to_addresses = apply_context_to_string(to_addresses, context, True)
            cc_addresses = apply_context_to_string(temp.cc_addresses, context, True)
            bcc_addresses = apply_context_to_string(temp.bcc_addresses, context, True)
            # https://docs.djangoproject.com/en/1.11/topics/Report/
            try:
                Report = ReportMultiAlternatives(
                    subject = subject,
                    body = plain_content,
                    from_Report = from_Report,
                    to = to_addresses,
                    cc = cc_addresses,
                    bcc = bcc_addresses,
                )
                Report.attach_alternative(html_content, "text/html")
                Report.send(False)
                msg_once_only(request, 'Report sent to ' + str(to_addresses), settings.SUCC_MSG_TYPE)
            except Exception as e:
                msg_once_only(request, 'Failed to Report ' + str(to_addresses) + ' as an exception occurred: ' + str(e), settings.ERR_MSG_TYPE)
        else:
            msg_once_only(request, 'Failed to Report as no valid template id was found for id: ' + template_id, settings.ERR_MSG_TYPE)
    else:
        msg_once_only(request, 'Failed to Report as no valid template id was provided', settings.ERR_MSG_TYPE)

def apply_agency_details_to_context(context):
    context['agency_name'] = config.AGENCY_NAME
    context['gen_con_from_address'] = config.GEN_CONTRACT_FROM_Report_ADDRESS

# run str through template to replace template variables - ie the stuff inside {{ }}
def apply_context_to_string(str, context, return_as_list = False):
    str_tpl = Template(str)
    str_with_context_applied = str_tpl.render(Context(context))
    return str_with_context_applied.split(",") if return_as_list else str_with_context_applied

