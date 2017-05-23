from django import forms
from django.core.validators import validate_email
from django.conf import settings

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


class AuditableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []

    class Meta:
        abstract = True
        fields = ('modified_by', 'modified_on', 'created_on', 'created_by')
        widgets = {
            'created_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
            'modified_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),}

    def prepare_required_field(self, field, label):
        self.fields[field].label = label + '*'
        self.fields[field].required = False