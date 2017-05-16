from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Client, Note, Address
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from .forms import ClientForm, NoteForm, ExampleForm, ExampleFormSetHelper, NoteFormSetHelper, AddressForm
from django import forms
from common.views import form_errors_as_array, super_user_or_job_coach
from django.contrib.auth.decorators import login_required, user_passes_test

def home_page(request):
    return render(request, 'client/home_page.html', {})


@login_required
@user_passes_test(super_user_or_job_coach, 'client_man_login')
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})


@login_required
def client_new(request):
    return manage_client(request, None)


@login_required
def client_edit(request, pk):
    return manage_client(request, pk)


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
def manage_client(request, client_id=None):
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

        if client_form.is_valid() and notes_form_set.is_valid() and address_form.is_valid():
            # client save
            created_client = client_form.save(commit=False)
            # created_client.modified_by = request.user
            created_client.save()
            # save address
            address = address_form.save(commit=False)
            address.person = created_client
            address.save()
            # save notes
            instances = notes_form_set.save(commit=False)
            for instance in instances:
                instance.modified_by = request.user
                instance.save()
            action = '/client/' + str(created_client.id) + '/edit' + '/'
            return redirect(action)
    else:
        address_form = AddressForm(instance=address, prefix="address")
        client_form = ClientForm(instance=client, prefix="main")
        notes_form_set = NoteInlineFormSet(instance=client, prefix="nested")
    # crispy form helper for formsets
    note_helper = NoteFormSetHelper()

    # TODO: get this to merger with form erros from the other forms
    # TODO: get it to work!
    client_form_errors = form_errors_as_array(client_form)
    address_form_errors = form_errors_as_array(address_form)
    form_errors = client_form_errors + address_form_errors

    return render(request, 'client/client_edit.html', {'form': client_form, 'notes_form_set': notes_form_set,
                                                       'the_action_text': the_action_text,
                                                       'edit_form': is_edit_form, 'note_helper': note_helper,
                                                       'the_action': action, 'address_form': address_form,
                                                       'form_errors': form_errors})



def cf_example(request):
    form = ExampleForm()
    return render(request, 'client/cf_example.html', {'form' : form})

def cf_example2(request):
    ExampleFormSet = formset_factory(ExampleForm, extra=3)
    formset = ExampleFormSet()
    helper = ExampleFormSetHelper()
    return render(request, 'client/cf_example2.html', {'example_formset' : formset, 'helper': helper})


# http://stackoverflow.com/questions/29758558/inlineformset-factory-create-new-objects-and-edit-objects-after-created
# https://gist.github.com/ibarovic/3092910
# this allos basic 1->m with notes
def manage_client_works(request, client_id=None):
    if client_id is None:
        client = Client()
        the_action_text = 'Create'
        is_edit_form = False
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=2, can_delete=False)
    else:
        the_action_text = 'Edit'
        is_edit_form = True
        client = get_object_or_404(Client, pk=client_id)
        NoteInlineFormSet = inlineformset_factory(Client, Note, form=NoteForm, extra=2, can_delete=True)

    if request.method == "POST":
        if request.POST.get("delete_client"):
            client = get_object_or_404(Client, pk=client_id)
            client.delete()
            return redirect('/client_list')
        form = ClientForm(request.POST, request.FILES, instance=client, prefix="main")
        formset = NoteInlineFormSet(request.POST, request.FILES, instance=client, prefix="nested")

        if form.is_valid() and formset.is_valid():
            created_client = form.save(commit=False)
            created_client.modified_by = request.user
            created_client.modified_date = timezone.now()
            created_client.save()
            formset.save()
            #return redirect('/bookauthor/formset')
    else:
        form = ClientForm(instance=client, prefix="main")
        formset = NoteInlineFormSet(instance=client, prefix="nested")

    return render(request, 'client/client_edit.html', {'form': form, 'notes_form_set': formset, 'the_action_text' : the_action_text, 'edit_form' : is_edit_form})

