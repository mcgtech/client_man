from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404
from client.forms import *
from common.views import *
from django.shortcuts import render
import json
from django.forms import inlineformset_factory

@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def interview_new(request, client_pk):
    return manage_interview(request, client_pk)


@login_required
@user_passes_test(access_client_details, 'client_man_login')
def interview_edit(request, client_pk, interview_id):
    return manage_interview(request, client_pk, interview_id)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
# TODO: suss if I should be using https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html in this fn
@transaction.atomic
def manage_interview(request, client_id, interview_id=None):
    client = get_object_or_404(Client, pk=client_id)
    extra_quals = 0
    if interview_id is None:
        extra_quals = 1
        interview = Interview()
        the_action_text = 'Create'
        is_edit_form = False
        QualInlineFormSet = inlineformset_factory(Interview, Qualification, form=QualificationForm, extra=extra_quals, can_delete=False)
        action = '/interview/' + str(client_id) + '/new/'
        display_client_summary_message(client, request, 'Adding a new interview for', settings.WARN_MSG_TYPE)
    else:
        interview = get_object_or_404(Interview, pk=interview_id)
        the_action_text = 'Edit'
        is_edit_form = True
        action = get_interview_edit_url(client_id, interview_id)
        # if inte has no quals then we need to have one blank one for the formset js code to work
        quals = Qualification.objects.filter(interview_id=interview_id)
        if len(quals) == 0:
            extra_quals = 1
        QualInlineFormSet = inlineformset_factory(Interview, Qualification, form=QualificationForm, extra=extra_quals, can_delete=True)

    del_request = handle_delete_request(request, client, interview, 'You have successfully deleted the interview ' + str(interview), '/client_search');
    if del_request:
        return del_request
    elif request.method == "POST":
        interview_form = InterviewForm(request.POST, request.FILES, instance=interview, prefix="interview", is_edit_form=is_edit_form, cancel_url=None, add_interview=is_edit_form)
        qual_form_set = QualInlineFormSet(request.POST, request.FILES, instance=interview, prefix="quals")
        if interview_form.is_valid() and qual_form_set.is_valid():
            created_interview = interview_form.save(commit=False)
            apply_auditable_info(created_interview, request)
            created_interview.client = client
            created_interview.save()
            interview = created_interview
            save_many_relationship(qual_form_set)
            msg_once_only(request, 'Saved interview for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)
            action = get_interview_edit_url(client_id, interview.id)
            return redirect(action)
    else:
        display_client_summary_message(client, request, 'Interview for ', settings.INFO_MSG_TYPE)
        cancel_url = redirect('client_edit', pk=client.id).url
        interview_form = InterviewForm(instance=interview, prefix="interview", is_edit_form=is_edit_form, cancel_url=cancel_url, add_interview=is_edit_form)
        qual_form_set = QualInlineFormSet(instance=interview, prefix="quals")

    qual_helper = QualificationFormSetHelper()
    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (acced via data_from_django in js)
    js_dict = {}
    add_interview_js_data(js_dict, client)
    set_deletion_status_in_js_data(js_dict, request.user, job_coach_man_user)
    js_data = json.dumps(js_dict)

    interview_form_errors = form_errors_as_array(interview_form)

    return render(request, 'client/interview/interview_edit.html', {'form': interview_form, 'client' : client,
                                                                    'qual_form_set': qual_form_set, 'qual_helper': qual_helper,
                                                                    'the_action_text': the_action_text,
                                                                    'edit_form': is_edit_form, 'the_action': action,
                                                                    'form_errors': interview_form_errors, 'js_data' : js_data})

def save_many_relationship(form_set):
    for form in form_set.forms:
        if form.has_changed():
            if form in form_set.deleted_forms:
                form.instance.delete()
            else:
                form.save()

def add_interview_js_data(js_dict, client):
    js_dict['add_url'] = '/interview/' + str(client.id) + '/new/'

def get_interview_edit_url(client_id, interview_id):
    return '/interview/' + str(client_id) + '/' + str(interview_id) + '/edit' + '/'