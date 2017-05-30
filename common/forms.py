from django import forms
from django.core.validators import validate_email
from django.conf import settings
from common.views import display_client_summary_message
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
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


## goes hand in hand with common.models.Auditable
class AuditableForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_edit_form = kwargs.pop('is_edit_form')
        cancel_url = kwargs.pop('cancel_url')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("save record", "Save", css_class='save_butt'))
        if is_edit_form:
            self.helper.add_input(Submit("delete record", "Delete", css_class='btn btn-danger delete-btn'))
        else:
            if cancel_url is not None:
                cancel_onclick = "javascript:location.href = '" + cancel_url + "';"
                self.helper.add_input(Button("cancel add", "Cancel", css_class='btn btn-default cancel-btn', onclick=cancel_onclick))
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []        # Note: if I use 'disabled' then the post returns nothing for the fields
        self.fields['modified_on'].widget.attrs['readonly'] = True
        self.fields['created_on'].widget.attrs['readonly'] = True
        # the form will not post values for these, so I need to remove
        # the disabled setting before saving - see setup_client_form()
        self.fields['modified_by'].widget.attrs['disabled'] = True
        self.fields['created_by'].widget.attrs['disabled'] = True

    class Meta:
        abstract = True
        widgets = {
            'created_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
            'modified_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),}


    def prepare_required_field(self, field, label):
        self.fields[field].label = label + '*'
        self.fields[field].required = False


def get_auditable_fields():
    return ('modified_by', 'modified_on', 'created_on', 'created_by')


def handle_delete_request(request, client, target, msg, url):
    redir = None
    if target is not None and request.POST.get("delete-record"):
        display_client_summary_message(client, request, msg, settings.INFO_MSG_TYPE)
        target.delete()
        redir = redirect(url)

    return redir
