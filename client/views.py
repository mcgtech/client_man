from django.shortcuts import redirect, render, get_object_or_404
from .models import Person, Client, Note, Address
from django.forms import inlineformset_factory
from .forms import ClientForm, NoteForm, NoteFormSetHelper, AddressForm
from django import forms
from common.views import form_errors_as_array, super_user_or_job_coach, super_user_or_admin, show_form_error
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
import json
from django.http import HttpResponse
import json

@login_required
@user_passes_test(super_user_or_admin, 'client_man_login')
def load_clients(request):
    json_data = open('static/json/clients.json')
    # deserialises it
    # need to eset created and last modified date
    json_clients = json.load(json_data)

    # TODO: chekc if client already exisits
    # TODO: trim strings
    # TODO: how to handle 'null'
    # TODO: I can pass the json obj directly into client contructor: http://stackoverflow.com/questions/21858465/json-file-reading-by-django
    # TODO: how will I handle addresses..
    # Create model instances for each item
    items = []

    Client.objects.all().delete()
    
    for json_client in json_clients:
        # create model instances...
        created_by = User.objects.get(id=json_client['created_by'])
        modified_by = User.objects.get(id=json_client['modified_by'])
        client = Client()
        client.type = Person.CLIENT

        client.title = get_clean_json_data(json_client['title'])
        client.middle_name = get_clean_json_data(json_client['middle_name'])
        client.known_as = get_clean_json_data(json_client['known_as'])
        client.dob = get_clean_json_data(json_client['dob'])
        client.forename = get_clean_json_data(json_client['forename'])
        client.surname = get_clean_json_data(json_client['surname'])
        client.email_address = get_clean_json_data(json_client['email_address'])
        client.created_by = created_by
        client.modified_by = modified_by
        client.sex = get_clean_json_data(json_client['sex'])
        client.known_as = get_clean_json_data(json_client['known_as'])
        client.marital_status = get_clean_json_data(json_client['marital_status'])
        client.ethnicity = get_clean_json_data(json_client['ethnicity'])
        client.save()
        items.append(client)

    # Create all in one query
    # Client.objects.bulk_create(items)

    return render(request, 'client/load_clients.html', {'json_clients': json_clients, 'items' : items})

def get_clean_json_data(json_data):
    if json_data is None:
        json_data = ''
    return json_data.strip()

def home_page(request):
    return render(request, 'client/home_page.html', {})

# code in view which returns json data
# http://www.lalicode.com/post/5/
@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def quick_client_search(request):
  if request.is_ajax():
    term = request.GET.get('term', '')
    if term:
        if term.isdigit():
            # TODO: hunt down Client.objects.select_related('user') and put into a function
            clients = Client.objects.select_related('user').filter(pk = term)
        else:
            clients = Person.find_person_by_full_name(term)
    else:
        clients = Client.objects.all()
    results = []
    # TODO: add name of coach at end od full name (do this inside the Client model class)
    for client in clients:
        client_json = {}
        client_json['id'] = client.id
        client_json['label'] = client.get_full_name()
        client_json['value'] = client.get_full_name()
        results.append(client_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'

  return HttpResponse(data, mimetype)


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_search(request):
    # this is simply getting all clients and then filtering client side using the js helper: https://www.datatables.net/
    # if this becomes a perf problem then read: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
    # note however that https://www.datatables.net/ can use ajax to reduce no of client returned, if I go down this pass then consider
    # using https://github.com/shymonk/django-datatable
    #
    # https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html
	clients = Client.objects.select_related('user').all()
	return render(request, 'search/client_search.html', {'clients' : clients})


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
    # TODO: suss if I should be using https://simpleisbetterthancomplex.com/tips/2016/05/16/django-tip-3-optimize-database-queries.html in this fn
    extra_notes = 0
    if client_id is None:
        extra_notes = 1
        client = Client()
        address = Address()
        the_action_text = 'Create'
        is_edit_form = False
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=extra_notes, can_delete=False)
        action = '/client/new/'
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        client = get_object_or_404(Client, pk=client_id)
        addresses = Address.objects.filter(person_id=client_id)
        if len(addresses) == 1:
            address = addresses[0]
        else:
            address = None
            show_form_error(request, messages, 'Expected a single address and found ' + str(len(addresses)) + ' instead', True)
        action = '/client/' + str(client_id) + '/edit' + '/'
        # if client has no notes then we need to have one blank one for the formset js code to work
        notes = Note.objects.filter(person_id=client_id)
        if len(notes) == 0:
            extra_notes = 1
        else:
            # need to suss this better
            note = notes[0]
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=extra_notes, can_delete=True)

    if request.method == "POST":
        if request.POST.get("delete-client"):
            client = get_object_or_404(Client, pk=client_id)
            # client.delete()
            # https://simpleisbetterthancomplex.com/tips/2016/09/06/django-tip-14-messages-framework.html
            messages.success(request, 'You have successfully deleted the client ' + client.get_full_name())
            return redirect('/client_search')
        client_form = ClientForm(request.POST, request.FILES, instance=client, prefix="main")
        address_form = AddressForm(request.POST, request.FILES, instance=address, prefix="address")
        notes_form_set = NoteInlineFormSet(request.POST, request.FILES, instance=client, prefix="nested")

        user = handle_client_user(request, client, client_form)
        if client_form.is_valid() and address_form.is_valid() and notes_form_set.is_valid():
            # TODO link changes to user made via admin into Person forename, surname... via listener
            created_client = save_client_details(client_form, user, request)
            save_client_address(address_form, created_client)
            save_client_notes(notes_form_set, request)
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


# remove request, client_from_db is not required
def save_client_details(client_form, user, request):
    created_client = client_form.save(commit=False)
    created_client.user = user
    apply_auditable_info(created_client, request)
    created_client.save()

    return created_client

# the dates and user from the form will be blank so we need to also pass the stored entity
# so we can retrieve the created date and user
def apply_auditable_info(form_created_entity, request):
    # only set when first created
    if form_created_entity.pk is None:
        form_created_entity.created_on = timezone.now()
        form_created_entity.created_by = request.user
    form_created_entity.modified_on = timezone.now()
    form_created_entity.modified_by = request.user


def save_client_address(address_form, client):
    address = address_form.save(commit=False)
    address.person = client
    address.save()


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