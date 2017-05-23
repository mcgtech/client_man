from django.conf import settings
from django.shortcuts import render

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