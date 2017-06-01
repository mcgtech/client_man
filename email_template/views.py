from django.conf import settings
from common.views import msg_once_only
from django.core.mail import EmailMultiAlternatives
from .models import EmailTemplate
from django.template import Context, Template
import json
from braces.views import GroupRequiredMixin
from .filters import EmailTempFilter
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import SingleTableView
from constance import config

from client.forms import *
from common.views import *
from .tables import EmailTempTable
from .forms import EmailTemplateForm


# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class EmailTempSearch(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = u"job coach"
    model = EmailTemplate
    table_class = EmailTempTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = EmailTempFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='email_template_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 15}
    context_table_name = 'email_temp_table'


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def email_temp_new(request):
    return manage_email_temp(request, None)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def email_temp_edit(request, pk):
    return manage_email_temp(request, pk)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def email_temp_test(request, temp_id, client_id):
    temp = EmailTemplate.objects.get(template_identifier=temp_id)
    client = get_object_or_404(Client, pk=client_id)
    context = {'client': client, 'contract' : contract, 'new_state' : None}
    send_email_using_template(context, temp_id, request)
    return render(request, 'email_test.html')


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_email_temp(request, temp_id=None):
    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (accessed via data_from_django in js)
    js_dict = {}
    if temp_id is None:
        temp = EmailTemplate()
        the_action_text = 'Create'
        is_edit_form = False
        action = '/email_temp/new/'
        msg_once_only(request, 'Adding a new template', settings.WARN_MSG_TYPE)
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        temp = get_object_or_404(EmailTemplate, pk=temp_id)
        action = '/email_temp/' + str(temp_id) + '/edit' + '/'

    if request.method == "POST":
        if request.POST.get("delete-record"):
            msg_once_only(request, 'You have successfully deleted the template ' + str(temp), settings.INFO_MSG_TYPE)
            temp.delete()
            return redirect('/email_temp_search')
        temp_form = EmailTemplateForm(request.POST, request.FILES, instance=temp, prefix="main", is_edit_form=is_edit_form, cancel_url=None)
        if temp_form.is_valid():
            temp = temp_form.save(commit=False)
            apply_auditable_info(temp, request)
            temp.save()
            action = '/email_temp/' + str(temp.id) + '/edit' + '/'
            msg_once_only(request, 'Saved template ' + str(temp), settings.INFO_MSG_TYPE)
            return redirect(action)
    else:
        cancel_url = redirect('email_temp_search').url
        temp_form = EmailTemplateForm(instance=temp, prefix="main", is_edit_form=is_edit_form, cancel_url=cancel_url)

    set_deletion_status_in_js_data(js_dict, request.user, admin_user)
    js_data = json.dumps(js_dict)

    temp_form_errors = form_errors_as_array(temp_form)

    return render(request, 'email_template.html', {'form': temp_form,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form,
                                                       'the_action': action, 'js_data' : js_data,
                                                       'form_errors': temp_form_errors,
                                                        'client_reflections' : get_client_reflections()})

def send_email_using_template(context, template_id, request, show_message = True):
    if template_id is not None:
        temp = EmailTemplate.objects.get(template_identifier=template_id)
        if temp is not None:
            apply_agency_details_to_context(context)
            # run body through template to replace template variables - ie the stuff inside {{ }}
            html_content = apply_context_to_string(temp.html_body, context)
            plain_content = apply_context_to_string(temp.plain_body, context)
            subject = apply_context_to_string(temp.subject, context)
            from_email = apply_context_to_string(temp.from_address, context)
            temp.to_addresses = 'mcgonigalstephen@gmail.com'
            to_addresses = apply_context_to_string(temp.to_addresses, context, True)
            cc_addresses = apply_context_to_string(temp.cc_addresses, context, True)
            bcc_addresses = apply_context_to_string(temp.bcc_addresses, context, True)
            # https://docs.djangoproject.com/en/1.11/topics/email/
            try:
                email = EmailMultiAlternatives(
                    subject = subject,
                    body = plain_content,
                    from_email = from_email,
                    to = to_addresses,
                    cc = cc_addresses,
                    bcc = bcc_addresses,
                )
                email.attach_alternative(html_content, "text/html")
                email.send(False)
                if show_message:
                    msg_once_only(request, 'Email sent to ' + str(to_addresses), settings.SUCC_MSG_TYPE)
            except Exception as e:
                msg_once_only(request, 'Failed to email ' + str(to_addresses) + ' as an exception occurred: ' + str(e), settings.ERR_MSG_TYPE)
        else:
            msg_once_only(request, 'Failed to email as no valid template id was found for id: ' + template_id, settings.ERR_MSG_TYPE)
    else:
        msg_once_only(request, 'Failed to email as no valid template id was provided', settings.ERR_MSG_TYPE)

def apply_agency_details_to_context(context):
    context['agency_name'] = config.AGENCY_NAME
    context['gen_con_from_address'] = config.GEN_CONTRACT_FROM_EMAIL_ADDRESS

# run str through template to replace template variables - ie the stuff inside {{ }}
def apply_context_to_string(str, context, return_as_list = False):
    str_tpl = Template(str)
    str_with_context_applied = str_tpl.render(Context(context))
    return str_with_context_applied.split(",") if return_as_list else str_with_context_applied

def get_client_reflections():
    from django.contrib.auth.models import User
    client_reflections = get_reflections(Client._meta, 'client')
    phone_reflections = get_reflections(Telephone._meta, 'client.telephone')
    address_reflections = get_reflections(Address._meta, 'client.address')
    contract_reflections = get_reflections(Contract._meta, 'client.get_latest_contract')
    status_reflections = get_reflections(Contract._meta, 'client.get_latest_contract.get_latest_status')
    user_reflections = get_reflections(User._meta, 'client.user')

    return client_reflections + contract_reflections + status_reflections + phone_reflections + address_reflections + user_reflections

def get_reflections(meta, prefix):
    refs = []
    for f in meta.get_fields(include_parents=True, include_hidden=True):
        name = f.name
        if f.get_internal_type() == 'IntegerField' and f.choices is not None and len(f.choices) > 0:
            name = 'get_' + name + '_display'
        elif f.get_internal_type() == 'BooleanField':
            name = name + '|yesno:"Yes,No"'
        refs.append('{{ ' + prefix + '.' + name + ' }}')
    return refs
