from django.shortcuts import redirect, get_object_or_404
from client.models import Client, TIOContract, ContractStatus
from common.models import Note, Address, Telephone
from django.forms import inlineformset_factory
from client.forms import *
from common.views import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from client.views import add_contract_js_data
import json

@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def contract_detail(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    return render(request, 'client/contract_detail.html', {'client': client})


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def contract_new(request, client_pk, con_type):
    con_type = int(con_type)
    return manage_contract(request, client_pk, con_type)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def contract_edit(request, client_pk, contract_id):
    return manage_contract(request, client_pk, None, contract_id)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
# TODO: suss if I should be using https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html in this fn
@transaction.atomic
def manage_contract(request, client_id, con_type, contract_id=None):
    status_list = None
    client = get_object_or_404(Client, pk=client_id)
    if contract_id is None:
        contract = get_contract_object(con_type, contract_id, None)
        the_action_text = 'Create'
        is_edit_form = False
        action = '/contract/' + str(client_id) + '/new/' + str(con_type) + '/'
        display_client_summary_message(client, request, 'Adding a new contract for', settings.WARN_MSG_TYPE)
    else:
        # load base contract so we can get its type
        base_contract = get_object_or_404(Contract, pk=contract_id)
        con_type = int(base_contract.type)
        the_action_text = 'Edit'
        is_edit_form = True
        contract = get_contract_object(con_type, contract_id, base_contract)
        action = get_contract_edit_url(client_id, contract_id)
        status_list = contract.get_ordered_status()
        curr_state = status_list.first().get_status_display() if status_list is not None else ''
        display_client_summary_message(client, request, 'Contract currently ' + curr_state + ' for ', settings.INFO_MSG_TYPE)

    del_request = handle_delete_request(request, client, contract, 'You have successfully deleted the contract ' + str(contract), '/client_search');
    if del_request:
        return del_request
    elif request.method == "POST":
        contract_form = get_contract_form(con_type, request, contract, "contract", is_edit_form, None, is_edit_form)
        if contract_form.is_valid():
            created_contract = contract_form.save(commit=False)
            apply_auditable_info(created_contract, request)
            created_contract.client = client
            created_contract.save()
            contract = created_contract
            # if newly created contract then add a defautl status of awaiting info man approval
            if contract_id is None:
                add_new_contract_state(request, contract, ContractStatus.AWAIT_INFO_MAN_ACC)
            action = get_contract_edit_url(client_id, contract.id)

            if request.POST.get("accept-contract"):
                handle_contract_accept(request, client, contract)
            elif request.POST.get("approve-contract"):
                handle_contract_approval(request, client, contract)
            elif request.POST.get("revoke-contract-approval"):
                handle_contract_approval_revoked(request, client, contract)
            elif request.POST.get("reject-contract"):
                handle_contract_rejection(request, client, contract)
            else:
                msg_once_only(request, 'Saved contract for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)
            return redirect(action)
    else:
        cancel_url = redirect('client_edit', pk=client.id).url
        contract_form = get_contract_form(con_type, request, contract, "contract", is_edit_form, cancel_url, is_edit_form)

    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (acced via data_from_django in js)
    js_dict = {}
    add_contract_js_data(js_dict, client)
    set_deletion_status_in_js_data(js_dict, request.user, job_coach_man_user)
    js_data = json.dumps(js_dict)

    state_buttons = get_state_buttons_to_display(client, con_type, is_edit_form, request)

    status_list = contract.get_ordered_status() if status_list is None else status_list

    contract_form_errors = form_errors_as_array(contract_form)
    return render(request, 'client/contract/contract_edit.html', {'form': contract_form, 'client' : client,
                                                                  'status_list' : status_list,
                                                                  'the_action_text': the_action_text,
                                                                  'edit_form': is_edit_form, 'the_action': action,
                                                                  'form_errors': contract_form_errors, 'js_data' : js_data,
                                                                  'contract_choices': Contract.TYPES, 'state_buttons' : state_buttons,
                                                                  'display_accept' : settings.DISPLAY_ACCEPT,
                                                                  'display_approve' : settings.DISPLAY_APPROVE,
                                                                  'display_reject' : settings.DISPLAY_REJECT,
                                                                  'display_revoke' : settings.DISPLAY_REVOKE})


def handle_contract_accept(request, client, contract):
    new_state = add_new_contract_state(request, contract, ContractStatus.ACC_INFO_MAN)
    handle_state_change(request, client, contract, new_state)
    msg_once_only(request, 'Accepted contract for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)


def handle_contract_approval(request, client, contract):
    new_state = add_new_contract_state(request, contract, ContractStatus.APP_FUND_MAN)
    handle_state_change(request, client, contract, new_state)
    msg_once_only(request, 'Approved contract for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)


def handle_contract_approval_revoked(request, client, contract):
    new_state = add_new_contract_state(request, contract, ContractStatus.ACC_REV_INFO_MAN)
    handle_state_change(request, client, contract, new_state)
    msg_once_only(request, 'Revoked approved contract for ' + client.get_full_name(), settings.WARN_MSG_TYPE)


def handle_contract_rejection(request, client, contract):
    new_state = add_new_contract_state(request, contract, ContractStatus.REJ_FUND_MAN)
    handle_state_change(request, client, contract, new_state)
    msg_once_only(request, 'Rejected contract for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)


def handle_state_change(request, client, contract, new_state):
    # https://github.com/vintasoftware/django-templated-email
    template = None
    context = {'client': client}
    if new_state.status == ContractStatus.ACC_INFO_MAN:
        template = 'approved_by_info_man'
        # TODO: get this to work correctly
        from_email='from@example.com',
        recipient_list=['mcgonigalstephen@gmail.com'],
    elif new_state.status == ContractStatus.ACC_REV_INFO_MAN:
        template = 'approval_cancelled_by_info_man'
        # TODO: get this to work correctly
        from_email='from@example.com',
        recipient_list=['mcgonigalstephen@gmail.com'],
    send_email_using_template(from_email, recipient_list, context, template, request)



def add_new_contract_state(request, contract, status):
    con_state = ContractStatus(contract=contract, status=status)
    apply_auditable_info(con_state, request)
    con_state.save()

    return con_state


def get_state_buttons_to_display(client, con_type, is_edit_form, request):
    buttons = []
    if is_edit_form:
        latest_con_state = client.get_latest_contract_state()
        if latest_con_state is not None:
            status = latest_con_state.status
            if contract_can_be_accepted(status):
                if info_man_user(request.user):
                    buttons.append(settings.DISPLAY_ACCEPT)
            elif contract_can_be_revoked(status):
                if info_man_user(request.user):
                    buttons.append(settings.DISPLAY_REVOKE)

            if type == Contract.TIO:
                if contract_can_be_approved(status):
                    if partner_user(request.user):
                        buttons.append(settings.DISPLAY_APPROVE)
                        buttons.append(settings.DISPLAY_REJECT)

    return buttons


def contract_can_be_accepted(status):
    return status == ContractStatus.AWAIT_INFO_MAN_ACC or status == ContractStatus.ACC_REV_INFO_MAN or status == ContractStatus.REJ_FUND_MAN;


def contract_can_be_revoked(status):
    return status == ContractStatus.ACC_INFO_MAN or status == ContractStatus.AWAIT_FUND_APP_MAN

def contract_can_be_approved(status):
    return status == ContractStatus.ACC_INFO_MAN or status == ContractStatus.AWAIT_FUND_APP_MAN



def get_contract_object(type, contract_id, base_contract):
    if type == Contract.TIO:
        if contract_id is None:
            contract = TIOContract()
        else:
            contract = get_object_or_404(TIOContract, pk=contract_id)
    else:
        if contract_id is None:
            contract = Contract()
        else:
            # if we have already loaded base contract to get the type then use it here
            contract = get_object_or_404(Contract, pk=contract_id) if base_contract is None else base_contract
    contract.type = type

    return contract


def get_contract_form(type, request, contract, prefix, is_edit_form, cancel_url, add_contract):
    if type == Contract.TIO:
        if request.method == "POST":
            contract_form = TIOContractForm(request.POST, request.FILES, instance=contract, prefix="contract", is_edit_form=is_edit_form, cancel_url=None, add_contract=is_edit_form)
        else:
            contract_form = TIOContractForm(instance=contract, prefix=prefix, is_edit_form=is_edit_form, cancel_url=cancel_url, add_contract=add_contract)
    else:
        if request.method == "POST":
            contract_form = ContractForm(request.POST, request.FILES, instance=contract, prefix="contract", is_edit_form=is_edit_form, cancel_url=None, add_contract=is_edit_form)
        else:
            contract_form = ContractForm(instance=contract, prefix=prefix, is_edit_form=is_edit_form, cancel_url=cancel_url, add_contract=add_contract)

    return contract_form

def get_contract_edit_url(client_id, contract_id):
    return '/contract/' + str(client_id) + '/' + str(contract_id) + '/edit' + '/'