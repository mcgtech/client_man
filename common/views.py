from django.conf import settings
from django.shortcuts import render
from django.utils import timezone

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


def super_user_or_admin(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists()


def super_user_or_job_coach(user):
    return user.is_superuser or user.groups.filter(name=settings.ADMIN_GROUP).exists() or user.groups.filter(name=settings.JOB_COACH).exists()


def show_form_error(request, messages, msg, inform_support):
    messages.error(request, msg)

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
        link = 'Unknown'
    else:
        full_name = client.get_full_name()
        link = '<a href="/client/' + str(client.id) + '/edit">' + full_name + '</a>'

    return link

def get_client_summary_link(client):
    name_link = get_client_name_link(client)

    return name_link + ' age: ' + str(client.age)