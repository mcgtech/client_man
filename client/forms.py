from django import forms
from .models import Client, Note, Address
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import validate_required_field, is_email_valid
from django.conf import settings


# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class ClientForm(forms.ModelForm):
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Main',
                Div('title',
                'sex',
                'forename',
                'middle_name',
                'surname',
                'known_as',
                css_class="col-sm-6"),
                Div('dob',
                'birth_certificate',
                'marital_status',
                'ethnicity',
                'modified_by',
                'modified_date',
                css_class="col-sm-6")
            ),
            Tab(
                'Project',
                'type',
                'social_work_involved'
            ),
            Tab(
                'User',
                'email_address',
                'username',
                'password'
            )
        )
    )
    helper.form_tag = False
    helper.add_input(Submit("save client", "Save"))
    helper.add_input(Submit("delete client", "Delete", css_class='btn btn-danger'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['forename'].label = "First Name*"
        self.fields['surname'].label = "Last Name*"
        self.fields['dob'].label = "Date of Birth*"
        self.fields['modified_by'].widget.attrs['disabled'] = True
        self.fields['modified_date'].widget.attrs['disabled'] = True


    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_forename(self):
        return validate_required_field(self, 'forename', 'first name')

    def clean_surname(self):
        return validate_required_field(self, 'surname', 'last name')

    def clean_dob(self):
        return validate_required_field(self, 'dob', 'date of birth')

    def clean_email_address(self):
        email = self.cleaned_data['email_address']
        if email and not is_email_valid(email):
            error_msg = 'email address is not valid'
            self.form_errors.append(error_msg)
            raise forms.ValidationError(error_msg)
        return email

    class Meta:
        model = Client
        fields = ('title', 'forename', 'middle_name', 'surname', 'known_as', 'dob', 'sex', 'email_address', 'modified_by',
                  'modified_date', 'birth_certificate', 'ethnicity', 'type', 'social_work_involved', 'marital_status')
        widgets = {
            'dob': forms.DateInput(attrs={'class':'datepicker'}),
            'modified_date': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),}


class AddressForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'line_3', 'post_code', 'area', 'evidence')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['line_1'].label = "Address line 1*"

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_line_1(self):
        return validate_required_field(self, 'line_1', 'line 1')


class NoteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modified_by'].widget.attrs['disabled'] = True
        self.fields['modified_date'].widget.attrs['disabled'] = True
        # self.helper.form_tag = True
    class Meta:
        model = Note
        fields = ('note', 'modified_by', 'modified_date', )
        widgets = {
            'modified_date': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),}


class NoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NoteFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'
