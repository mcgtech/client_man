import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from client.forms import *
from common.views import *


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client/client_detail.html', {'client': client})


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def client_new(request):
    return manage_client(request, None)


@login_required
@user_passes_test(job_coach_user, 'client_man_login')
def client_edit(request, pk):
    return manage_client(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_client(request, client_id=None):
    # TODO: suss if I should be using https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html in this fn
    extra_notes = 0
    extra_phones = 0
    # setup js variables for template
    #https://godjango.com/blog/working-with-json-and-django/
    # needs {% include 'partials/inject_js_data.html' %} added to template (accessed via data_from_django in js)
    js_dict = {}
    if client_id is None:
        extra_notes = 1
        extra_phones = 1
        client = Client()
        address = Address()
        the_action_text = 'Create'
        is_edit_form = False
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=extra_notes, can_delete=False)
        PhoneInlineFormSet = inlineformset_factory(Client, Telephone, form=PhoneForm, extra=extra_phones, can_delete=False)
        action = '/client/new/'
        msg_once_only(request, 'Adding a new client', settings.WARN_MSG_TYPE)
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        client = get_object_or_404(Client, pk=client_id)
        add_contract_js_data(js_dict, client)
        address = client.address
        action = '/client/' + str(client_id) + '/edit' + '/'
        # if client has no notes/phones then we need to have one blank one for the formset js code to work
        notes = Note.objects.filter(person_id=client_id)
        if len(notes) == 0:
            extra_notes = 1
        phones = Telephone.objects.filter(person_id=client_id)
        if len(phones) == 0:
            extra_phones = 1
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=extra_notes, can_delete=True)
        PhoneInlineFormSet = inlineformset_factory(Client, Telephone, form=PhoneForm, extra=extra_phones, can_delete=True)

    del_request = handle_delete_request(request, client, client, 'You have successfully deleted the client ' + client.get_full_name(), '/client_search');
    if del_request:
        return del_request
    elif request.method == "POST":
        client_form = ClientForm(request.POST, request.FILES, instance=client, prefix="main", is_edit_form=is_edit_form, cancel_url=None, add_contract=is_edit_form)
        address_form = AddressForm(request.POST, request.FILES, instance=address, prefix="address")
        notes_form_set = NoteInlineFormSet(request.POST, request.FILES, instance=client, prefix="nested")
        phone_form_set = PhoneInlineFormSet(request.POST, request.FILES, instance=client, prefix="phones")

        user = handle_client_user(request, client, client_form)
        if client_form.is_valid() and address_form.is_valid() and notes_form_set.is_valid() and phone_form_set.is_valid():
            # TODO link changes to user made via admin into Person forename, surname... via listener
            created_client = save_client_details(client_form, user, request)
            save_client_address(address_form, created_client)
            save_client_notes(notes_form_set, request)
            save_client_phones(phone_form_set, request)
            action = '/client/' + str(created_client.id) + '/edit' + '/'
            display_client_summary_message(client, request, 'Saved ' + client.get_full_name(), settings.INFO_MSG_TYPE)
            return redirect(action)
    else:
        cancel_url = redirect('client_search').url
        address_form = AddressForm(instance=address, prefix="address")
        client_form = ClientForm(instance=client, prefix="main", is_edit_form=is_edit_form, cancel_url=cancel_url, add_contract=is_edit_form)
        notes_form_set = NoteInlineFormSet(instance=client, prefix="nested")
        phone_form_set = PhoneInlineFormSet(instance=client, prefix="phones")
    # crispy form helper for formsets
    note_helper = NoteFormSetHelper()
    phone_helper = PhoneFormSetHelper()

    # https://docs.djangoproject.com/en/1.11/topics/db/queries/#limiting-querysets
    contracts = client.get_all_contracts_ordered()
    set_deletion_status_in_js_data(js_dict, request.user, job_coach_man_user)
    js_dict['client_id'] = client_id
    js_data = json.dumps(js_dict)

    client_form_errors = form_errors_as_array(client_form)
    address_form_errors = form_errors_as_array(address_form)
    form_errors = client_form_errors + address_form_errors

    return render(request, 'client/client/client_edit.html', {'form': client_form, 'client' : client,
                                                       'notes_form_set': notes_form_set, 'note_helper': note_helper,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form,
                                                       'the_action': action, 'address_form': address_form,
                                                       'phone_form_set': phone_form_set, 'phone_helper': phone_helper,
                                                        'contracts' : contracts, 'js_data' : js_data,
                                                       'form_errors': form_errors, 'contract_choices' : Contract.TYPES})

def add_contract_js_data(js_dict, client):
    js_dict['add_con_url'] = '/contract/' + str(client.id) + '/new/'


# remove request, client_from_db is not required
def save_client_details(client_form, user, request):
    created_client = client_form.save(commit=False)
    created_client.user = user
    apply_auditable_info(created_client, request)
    created_client.save()

    return created_client


def save_client_address(address_form, client):
    address = address_form.save(commit=False)
    address.person = client
    address.save()


def save_client_phones(phones_form_set, request):
    for note_form in phones_form_set.forms:
        if note_form.has_changed():
            if note_form in phones_form_set.deleted_forms:
                note_form.instance.delete()
            else:
                note_form.save()

def save_client_notes(notes_form_set, request):
    for note_form in notes_form_set.forms:
        if note_form.has_changed():
            if note_form in notes_form_set.deleted_forms:
                note_form.instance.delete()
            else:
                # for some reason modified_by and modified_date always come back as changed
                if 'note' in note_form.changed_data:
                    instance = note_form.save(commit=False)
                    instance.modified_date = timezone.now()
                    instance.modified_by = request.user
                    instance.save()


def handle_client_user(request, client, form):
    # todo send out email asking them to reset password
    user = None
    user_exists = False
    if client.user:
        user_exists = True

    if request.POST.get("main-username"):
        if request.POST.get("main-email_address"):
            if request.POST.get("main-password"):
                handle_client_user_storage(request, client, form, user_exists)
            else:
                if user_exists == False:
                    form.add_error('password', 'You must set a password to associate a user account') # causes form to be invalid
                else:
                    handle_client_user_storage(request, client, form, user_exists)
        else:
            form.add_error('email_address', 'You must set the email address if you have set username') # causes form to be invalid

    return user


def handle_client_user_storage(request, client, form, user_exists):
    user = None
    email_address = request.POST.get("main-email_address")
    username = request.POST.get("main-username")
    email_exists = User.objects.filter(email=email_address).exists()
    username_exists = User.objects.filter(username=username).exists()
    user_valid = True
    if user_exists == True:
        user = client.user
    else:
        if username_exists:
            user_valid = False
            set_username_in_use_form_error(form)
        if email_exists:
            user_valid = False
            set_email_in_use_form_error(form)
        if user_valid:
            password = request.POST.get("main-username")
            user = User.objects.create_user(username, email_address, password)
            client_group = Group.objects.get(name=settings.CLIENT_GROUP)
            client_group.user_set.add(user)
    if user_valid:
        if request.POST.get("main-password"):
            user.set_password(request.POST.get("main-password"))
        user.first_name = request.POST.get("forename")
        user.last_name = request.POST.get("surname")
        # need to ensure that we are not changing email and/or user name to one that someone else is using
        if client.email_address != email_address and email_exists:
            user_valid = False
            set_email_in_use_form_error(form)
        if client.username != username and username_exists:
            user_valid = False
            set_username_in_use_form_error(form)
        if user_valid:
            user.email = email_address
            user.email = username
            user.save()
            client.user = user

    return user


def set_email_in_use_form_error(form):
    form.add_error('email_address', 'This email address is already in use') # causes form to be invalid


def set_username_in_use_form_error(form):
    form.add_error('username', 'This username is already in use') # causes form to be invalid