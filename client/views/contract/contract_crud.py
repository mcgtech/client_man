from django.shortcuts import redirect, get_object_or_404
from client.models import Client
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

@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def contract_detail(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    return render(request, 'client/contract_detail.html', {'client': client})


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def contract_new(request, client_pk):
    return manage_contract(request, client_pk)


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def contract_edit(request, client_pk, contract_id):
    return manage_contract(request, client_pk, contract_id)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
# TODO: suss if I should be using https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html in this fn
@transaction.atomic
def manage_contract(request, client_id, contract_id=None):
    client = get_object_or_404(Client, pk=client_id)
    if contract_id is None:
        contract = Contract()
        the_action_text = 'Create'
        is_edit_form = False
        action = '/contract/' + str(client_id) + '/new/'
        display_client_summary_message(client, request, 'Add a new contract for')
    else:
        display_client_summary_message(client, request, 'Contract details for')
        the_action_text = 'Edit'
        is_edit_form = True
        contract = get_object_or_404(Contract, pk=contract_id)
        action = get_contract_edit_url(client_id, contract_id)
    if request.method == "POST":
        if request.POST.get("delete-contract"):
            contract.delete()
            msg_once_only(request, 'You have successfully deleted the contract ' + str(contract), settings.SUCC_MSG_TYPE)
            return redirect('/client_search')
        contract_form = ContractForm(request.POST, request.FILES, instance=contract, prefix="contract")
        if contract_form.is_valid():
            created_contract = contract_form.save(commit=False)
            apply_auditable_info(created_contract, request)
            created_contract.client = client
            created_contract.save()
            action = get_contract_edit_url(client_id, created_contract.id)
            msg_once_only(request, 'Saved contract for ' + client.get_full_name(), settings.SUCC_MSG_TYPE)
            return redirect(action)
    else:
        contract_form = ContractForm(instance=contract, prefix="contract")

    contract_form_errors = form_errors_as_array(contract_form)
    return render(request, 'client/contract/contract_edit.html', {'form': contract_form, 'client' : client,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form, 'the_action': action,
                                                       'form_errors': contract_form_errors})


def get_contract_edit_url(client_id, contract_id):
    return '/contract/' + str(client_id) + '/' + str(contract_id) + '/edit' + '/'