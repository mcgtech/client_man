from django import forms
from django.core.validators import validate_email
from django.conf import settings
from common.views import get_client_summary_link
from django.contrib.messages import info, success, warning, error, debug
from django.contrib.messages import get_messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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
        add_delete = kwargs.pop('add_delete')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("save contract", "Save"))
        if add_delete:
            self.helper.add_input(Submit("delete contract", "Delete", css_class='btn btn-danger delete-btn'))
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


def display_client_summary_message(client, request, prefix):
    msg_once_only(request, prefix + ' ' + get_client_summary_link(client), settings.INFO_MSG_TYPE)
    # messages.info(request, prefix + ' ' + get_client_summary_link(client))


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