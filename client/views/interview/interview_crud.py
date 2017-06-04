from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import get_object_or_404
from client.forms import *
from common.views import *
from django.shortcuts import render
import json
from django.forms import inlineformset_factory
from collections import namedtuple
from client.views import get_client_form_get_edit_config, get_extras_for_formset, get_client_form_add_url, save_many_relationship, get_client_form_edit_url, get_client_formset, save_client_primary_entity, get_client_js_data

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
@transaction.atomic
def manage_interview(request, client_id, interview_id=None):
    config = get_client_form_get_edit_config(interview_id, client_id, Interview, request)
    # formsets
    qual_form_set = get_client_formset(config, Interview, Qualification, QualificationForm, Qualification.objects.filter(interview_id=config.primary_id), "quals")
    qual_helper = QualificationFormSetHelper()

    del_request = handle_delete_request(request, config.client, config.primary_entity, 'You have successfully deleted the ' + config.class_name + ' ' + str(config.primary_entity), '/client_search');
    if del_request:
        return del_request
    elif request.method == "POST":
        primary_entity_form = InterviewForm(request.POST, request.FILES, instance=config.primary_entity, prefix=config.class_name, is_edit_form=config.is_edit_form, cancel_url=config.cancel_url, add_interview=config.is_edit_form)
        if primary_entity_form.is_valid() and qual_form_set.is_valid():
            created_primary_entity = save_client_primary_entity(request, primary_entity_form, config)
            save_many_relationship(qual_form_set)
            msg_once_only(request, 'Saved ' + config.class_name + ' for ' + config.client.get_full_name(), settings.SUCC_MSG_TYPE)
            action = get_client_form_edit_url(config.client.id, created_primary_entity.id, config.class_name)
            return redirect(action)
    else:
        display_client_summary_message(config.client, request, config.class_name.capitalize() + ' for ', settings.INFO_MSG_TYPE)
        primary_entity_form = InterviewForm(instance=config.primary_entity, prefix=config.class_name, is_edit_form=config.is_edit_form, cancel_url=config.cancel_url, add_interview=config.is_edit_form)


    interview_form_errors = form_errors_as_array(primary_entity_form)

    return render(request, 'client/interview/interview_edit.html', {'form': primary_entity_form,
                                                                    'qual_form_set': qual_form_set, 'qual_helper': qual_helper,
                                                                    'config' : config,
                                                                    'js_data': get_client_js_data(config, request),
                                                                    'form_errors': interview_form_errors, })

