from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404
from client.forms import *
from client.views import add_contract_js_data
from common.views import *
from django.shortcuts import render
from constance import config
import json
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin
from common.tables import HTMLTempTable
from common.filters import HTMLTempFilter
from django_tables2 import SingleTableView


# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class HTMLTempSearch(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = u"job coach"
    model = HTMLTemplate
    table_class = HTMLTempTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = HTMLTempFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='html_template_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 15}
    context_table_name = 'html_temp_table'


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def html_temp_new(request):
    return manage_html_temp(request, None)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def html_temp_edit(request, pk):
    return manage_html_temp(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_html_temp(request, temp_id=None):
    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (accessed via data_from_django in js)
    js_dict = {}
    if temp_id is None:
        temp = HTMLTemplate()
        the_action_text = 'Create'
        is_edit_form = False
        action = '/html_temp/new/'
        msg_once_only(request, 'Adding a new template', settings.WARN_MSG_TYPE)
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        temp = get_object_or_404(HTMLTemplate, pk=temp_id)
        action = '/html_temp/' + str(temp_id) + '/edit' + '/'

    if request.method == "POST":
        if request.POST.get("delete-record"):
            msg_once_only(request, 'You have successfully deleted the template ' + str(temp), settings.INFO_MSG_TYPE)
            temp.delete()
            return redirect('/html_temp_search')
        temp_form = HTMLTemplateForm(request.POST, request.FILES, instance=temp, prefix="main", is_edit_form=is_edit_form)
        if temp_form.is_valid():
            temp = temp_form.save(commit=False)
            apply_auditable_info(temp, request)
            temp.save()
            action = '/html_temp/' + str(temp.id) + '/edit' + '/'
            msg_once_only(request, 'Saved template ' + str(temp), settings.INFO_MSG_TYPE)
            return redirect(action)
    else:
        temp_form = HTMLTemplateForm(instance=temp, prefix="main", is_edit_form=is_edit_form)
    set_deletion_status_in_js_data(js_dict, request.user, admin_user)
    js_data = json.dumps(js_dict)

    temp_form_errors = form_errors_as_array(temp_form)

    return render(request, 'html_template.html', {'form': temp_form,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form,
                                                       'the_action': action, 'js_data' : js_data,
                                                       'form_errors': temp_form_errors})