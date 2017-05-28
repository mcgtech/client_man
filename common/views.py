from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from templated_email import send_templated_mail
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


def admin_user(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists()

def job_coach_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.JOB_COACH_MAN).exists()

def job_coach_user(user):
    return job_coach_man_user(user) or user.groups.filter(name=settings.JOB_COACH).exists()

def info_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.JOB_COACH).exists()

def partner_user(user):
    return info_man_user(user) or user.groups.filter(name=settings.PARTNER).exists()

# as seen in tio approval for shirlie staff
def supply_chain_man_user(user):
    return admin_user(user) or user.groups.filter(name=settings.SUPPLY_CHAIN_MAN).exists()

def supply_chain_partner_user(user):
    return admin_user(user) or user.groups.filter(name=settings.SUPPLY_CHAIN_PART).exists()

def show_form_error(request, messages, msg, inform_support):
    messages.error(request, msg)

def set_deletion_status_in_js_data(js_dict, user, security_fn):
    js_dict['delete_allowed'] = security_fn(user)

# the dates and user from the form will be blank so we need to also pass the stored entity
# so we can retrieve the created date and user
def apply_auditable_info(form_created_entity, request):
    # only set when first created
    if form_created_entity.pk is None:
        form_created_entity.created_on = timezone.now()
        form_created_entity.created_by = request.user
    form_created_entity.modified_on = timezone.now()
    form_created_entity.modified_by = request.user


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


def send_email_using_template(from_email, recipient_list, context, template, request):
    send_templated_mail(
        template_name=template,
        from_email=from_email,
        recipient_list=recipient_list,
        context=context,
        # Optional:
        # cc=['cc@example.com'],
        # bcc=['bcc@example.com'],
        # headers={'My-Custom-Header':'Custom Value'},
        # template_prefix="my_emails/",
        # template_suffix="email",
    )
    msg_once_only(request, 'Email sent to ' + str(recipient_list), settings.SUCC_MSG_TYPE)