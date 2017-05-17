from django.shortcuts import redirect, render, get_object_or_404
from .models import Client, Note, Address
from django.forms import inlineformset_factory
from .forms import ClientForm, NoteForm, NoteFormSetHelper, AddressForm
from django import forms
from common.views import form_errors_as_array, super_user_or_job_coach
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings

def home_page(request):
    return render(request, 'client/home_page.html', {})


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_list(request):
    # https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html
    clients = Client.objects.select_related('user').all()
    return render(request, 'client/client_list.html', {'clients': clients})


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_new(request):
    return manage_client(request, None)


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_edit(request, pk):
    return manage_client(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
@transaction.atomic
def manage_client(request, client_id=None):
    # TODO: use a listener to keep first and last name in sync - if user exists
    if client_id is None:
        client = Client()
        address = Address()
        the_action_text = 'Create'
        is_edit_form = False
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=2, can_delete=False)
        action = '/client/new/'
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        client = get_object_or_404(Client, pk=client_id)
        addresses = Address.objects.filter(person_id=client_id)
        if len(addresses) == 1:
            address = addresses[0]
            NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=2, can_delete=True)
            action = '/client/' + str(client_id) + '/edit' + '/'
        else:
            raise forms.ValidationError('Expected a single address and found ' + str(len(addresses)) + ' instead')

    if request.method == "POST":
        if request.POST.get("delete-client"):
            client = get_object_or_404(Client, pk=client_id)
            client.delete()
            return redirect('/client_list')
        client_form = ClientForm(request.POST, request.FILES, instance=client, prefix="main")
        address_form = AddressForm(request.POST, request.FILES, instance=address, prefix="address")
        notes_form_set = NoteInlineFormSet(request.POST, request.FILES, instance=client, prefix="nested")

        user = handle_client_user(request, client, client_form)
        if client_form.is_valid() and address_form.is_valid() and notes_form_set.is_valid():
            # client save
            # TODO link changes to user made via admin into Person forename, surname...
            # TODO: as I dont set any fields I can simply do a save with true
            created_client = client_form.save(commit=False)
            # created_client.changed_by = request.user
            created_client.user = user
            created_client.save()
            # save address
            address = address_form.save(commit=False)
            address.person = created_client
            address.save()
            # save notes
            instances = notes_form_set.save(commit=False)
            for instance in instances:
                #instance.changed_by = request.user
                instance.save()
            action = '/client/' + str(created_client.id) + '/edit' + '/'
            return redirect(action)
    else:
        address_form = AddressForm(instance=address, prefix="address")
        client_form = ClientForm(instance=client, prefix="main")
        notes_form_set = NoteInlineFormSet(instance=client, prefix="nested")
    # crispy form helper for formsets
    note_helper = NoteFormSetHelper()

    client_form_errors = form_errors_as_array(client_form)
    address_form_errors = form_errors_as_array(address_form)
    form_errors = client_form_errors + address_form_errors

    return render(request, 'client/client_edit.html', {'form': client_form, 'notes_form_set': notes_form_set,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form, 'note_helper': note_helper,
                                                       'the_action': action, 'address_form': address_form,
                                                       'form_errors': form_errors})


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