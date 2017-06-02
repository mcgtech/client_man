from django.conf import settings
from django.shortcuts import render
from django.contrib.messages import get_messages
from django.contrib.messages import info, success, warning, error, debug
from client.models import *
from common.models import *

# http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
def form_errors_as_array(form):
    errors = []
    if (form.errors and len(form.errors) > 0):
        for error in form.errors.items():
            errors.append(remove_html_tags(str(error[1])))

    return errors


def home_page(request):
    return render(request, 'home_page.html', {})

# https://jorlugaqui.net/2016/02/20/how-to-strip-html-tags-from-a-string-in-python/
def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def display_client_summary_message(client, request, prefix, msg_type):
    msg_once_only(request, prefix + ' ' + get_client_summary_link(client), msg_type)


def get_client_name_link(client):
    if client == None:
        link = 'Unknown client'
    else:
        full_name = client.get_full_name()
        link = '<a href="/client/' + str(client.id) + '/edit">' + full_name + '</a>'

    return link

def get_client_summary_link(client):
    name_link = get_client_name_link(client)

    return name_link + ' age: ' + str(client.age)


# https://stackoverflow.com/questions/23249807/django-remove-duplicate-messages-from-storage/25157660#25157660
def msg_once_only(request, msg, type):
    """
    Just add the message once
    :param request:
    :param msg:
    :return:
    """
    storage = get_messages(request)
    if msg not in [m.message for m in storage]:
        if (type == settings.INFO_MSG_TYPE):
            info(request, msg)
        elif (type == settings.SUCC_MSG_TYPE):
            success(request, msg)
        elif (type == settings.WARN_MSG_TYPE):
            warning(request, msg)
        elif (type == settings.ERR_MSG_TYPE):
            error(request, msg)
        elif (type == settings.DEBUG_MSG_TYPE):
            debug(request, msg)
    storage.used = False # to ensure we dont clear the messages we got in storage = get_messages(request)

def get_force_page_break_markup():
    return '<div style="display: block; page-break-after: always; position: relative;"></div>'


def get_client_reflections():
    from django.contrib.auth.models import User
    client_reflections = get_reflections(Client._meta, 'client')
    phone_reflections = get_reflections(Telephone._meta, 'telephone')
    address_reflections = get_reflections(Address._meta, 'address')
    note_reflections = get_reflections(Note._meta, 'note')
    contract_reflections = get_reflections(Contract._meta, 'client.get_latest_contract')
    status_reflections = get_reflections(Contract._meta, 'client.get_latest_contract.get_latest_status')
    user_reflections = get_reflections(User._meta, 'client.user')

    return client_reflections + contract_reflections + note_reflections + status_reflections + phone_reflections + address_reflections + user_reflections

def get_reflections(meta, prefix):
    refs = []
    for f in meta.get_fields(include_parents=True, include_hidden=True):
        name = prefix + '.' + f.name
        suffix = None
        open_brace = '{{ '
        close_brace = ' }}'
        if f.get_internal_type() == 'IntegerField' and f.choices is not None and len(f.choices) > 0:
            name = prefix + '.' + 'get_' + f.name + '_display'
        elif f.get_internal_type() == 'BooleanField':
            name = name + '|yesno:"Yes,No"'
        elif f.get_internal_type() == 'ForeignKey':
            name = 'for x in ' + name + '.all'
            suffix = '{{ x.abc }} {% endfor %} '
            open_brace = '{% '
            close_brace = ' %}'
        tag = open_brace + name + close_brace
        if suffix is not None:
            tag = tag + suffix
        refs.append(tag)
    return refs