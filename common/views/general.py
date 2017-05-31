from django.conf import settings
from django.shortcuts import render
from django.contrib.messages import get_messages
from django.contrib.messages import info, success, warning, error, debug

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
    if msg not in [m.message for m in get_messages(request)]:
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
