from django import forms
from django.core.validators import validate_email

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
