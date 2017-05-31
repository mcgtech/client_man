from django import forms
from django.core.validators import validate_email
from django.conf import settings
from common.views import display_client_summary_message
from django.shortcuts import redirect

def validate_required_field(self, field_name, field_name_desc):
    fld = self.cleaned_data[field_name]
    if not fld and fld != 0:
        error_msg = 'please enter a value for ' + field_name_desc
        self.form_errors.append(error_msg)
        raise forms.ValidationError(error_msg)
    return fld

def is_email_valid(email):
    try:
        validate_email( email )
        return True
    except forms.ValidationError:
        return False


def handle_delete_request(request, client, target, msg, url):
    redir = None
    if target is not None and request.POST.get("delete-record"):
        display_client_summary_message(client, request, msg, settings.INFO_MSG_TYPE)
        target.delete()
        redir = redirect(url)

    return redir
