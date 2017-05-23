from django import forms
from .models import Client
from common.models import Note, Address, Telephone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import validate_required_field, is_email_valid
from django.conf import settings

# forms for editting

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
                'forename',
                'middle_name',
                'surname',
                'known_as',
                'sex',
                css_class="col-sm-6"),
                Div(
                    # age is added directly in the template and manipulated via js
                    Div(Div('dob', css_class="col-sm-4"), Div('birth_certificate', css_class="col-sm-4"), css_class='row dob'),
                'marital_status',
                'ethnicity',
                'created_by',
                'created_on',
                'modified_by',
                'modified_on',
                css_class="col-sm-6")
            ),
            Tab(
                'Project',
                Div(
                    Div(Div('job_coach', css_class="col-sm-6"), Div('client_status', css_class="col-sm-6"), css_class='row'),
                Div(Div('start_date', css_class="col-sm-6"), Div('end_date', css_class="col-sm-6"), css_class='row'),
                    'nat_ins_number',
                'education',
                'jsa',
                'recommended_by', 'social_work_involved',
                css_class="col-sm-6"),
                Div(
                    Div(Div('client_group', css_class="col-sm-6"), Div('client_group_evidence', css_class="col-sm-6"), css_class='row'),
                    Div(Div('employment_status', css_class="col-sm-6"), Div('employment_status_evidence', css_class="col-sm-6"), css_class='row'),
                'time_unemployed',
                'stage',
                'ref_received',
                css_class="col-sm-6")
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
        self.fields['title'].label = "Title*"
        self.fields['client_status'].label = "Client status*"
        self.fields['forename'].label = "First Name*"
        self.fields['surname'].label = "Last Name*"
        self.fields['dob'].label = "Date of Birth*"
        self.fields['recommended_by'].label = "Recommended by*"
        self.fields['jsa'].label = "JSA*"
        self.fields['education'].label = "Education*"
        self.fields['client_group'].label = "Client group*"
        self.fields['time_unemployed'].label = "Time unemployed*"
        self.fields['client_group'].label = "Client group*"
        self.fields['job_coach'].label = "Job coach*"
        self.fields['sex'].label = "Sex*"
        self.fields['marital_status'].label = "Marital status*"
        self.fields['ethnicity'].label = "Ethnicity*"

        # Note: if I use 'disabled' then the post returns nothing for the fields
        self.fields['modified_on'].widget.attrs['readonly'] = True
        self.fields['created_on'].widget.attrs['readonly'] = True
        self.fields['start_date'].widget.attrs['readonly'] = True
        # the form will not post values for these, so I need to remove
        # the disabled setting before saving - see setup_client_form()
        self.fields['modified_by'].widget.attrs['disabled'] = True
        self.fields['created_by'].widget.attrs['disabled'] = True
        self.fields['education'].error_messages = {'required': 'Education is required'}

        self.fields['title'].required = False
        self.fields['recommended_by'].required = False
        self.fields['jsa'].required = False
        self.fields['education'].required = False
        self.fields['employment_status'].required = False
        self.fields['stage'].required = False
        self.fields['client_group'].required = False
        self.fields['time_unemployed'].required = False
        self.fields['client_group'].required = False
        self.fields['job_coach'].required = False
        self.fields['sex'].required = False
        self.fields['marital_status'].required = False
        self.fields['ethnicity'].required = False
        self.fields['client_status'].required = False


    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_title(self):
        return validate_required_field(self, 'title', 'title')

    def clean_client_status(self):
        return validate_required_field(self, 'client_status', 'client status')

    def clean_ethnicity(self):
        return validate_required_field(self, 'ethnicity', 'ethnicity')


    def clean_marital_status(self):
        return validate_required_field(self, 'marital_status', 'marital status')

    def clean_sex(self):
        return validate_required_field(self, 'sex', 'sex')

    def clean_forename(self):
        return validate_required_field(self, 'forename', 'first name')

    def clean_surname(self):
        return validate_required_field(self, 'surname', 'last name')

    def clean_dob(self):
        return validate_required_field(self, 'dob', 'date of birth')

    def clean_recommended_by(self):
        return validate_required_field(self, 'recommended_by', 'recommended by')

    def clean_jsa(self):
        return validate_required_field(self, 'jsa', 'JSA')

    def clean_education(self):
        return validate_required_field(self, 'education', 'education')

    def clean_time_unemployed(self):
        return validate_required_field(self, 'time_unemployed', 'time unemployed')

    def clean_client_group(self):
        return validate_required_field(self, 'client_group', 'client group')

    def clean_job_coach(self):
        return validate_required_field(self, 'job_coach', 'job coach')

    def clean_email_address(self):
        email = self.cleaned_data['email_address']
        if email and not is_email_valid(email):
            error_msg = 'email address is not valid'
            self.form_errors.append(error_msg)
            raise forms.ValidationError(error_msg)
        return email

    class Meta:
        model = Client
        fields = ('title', 'forename', 'middle_name', 'surname', 'known_as', 'dob', 'sex', 'email_address', 'job_coach',
                  'birth_certificate', 'ethnicity', 'social_work_involved', 'marital_status', 'employment_status_evidence'
                  ,'modified_by', 'modified_on', 'start_date', 'end_date'
                  ,'created_on', 'created_by', 'nat_ins_number', 'education', 'recommended_by', 'jsa', 'employment_status'
                  ,'time_unemployed', 'stage', 'client_group', 'ref_received', 'client_group_evidence', 'client_status'
                  )
        widgets = {
            'dob': forms.DateInput(attrs={'class':'datepicker'}),
            'created_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
            'modified_on': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
            'start_date': forms.DateInput(format=(settings.DISPLAY_DATE)),
            'end_date': forms.DateInput(format=(settings.DISPLAY_DATE)),}



class AddressForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout('line_1', 'line_2', 'line_3', 'post_code',
                    Div(Div('area', css_class="col-sm-6"), Div('evidence', css_class="col-sm-6"), css_class='row'),
                  )
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'line_3', 'post_code',
                 'area', 'evidence'
                  )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['line_1'].label = "Address line 1*"
        self.fields['area'].label = "Area*"
        self.fields['evidence'].label = "Area Evidence"

        self.fields['area'].required = False

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_line_1(self):
        return validate_required_field(self, 'line_1', 'line 1')

    def clean_area(self):
        return validate_required_field(self, 'area', 'area')

# one to many forms

class PhoneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = Telephone
        fields = ('type', 'number', )


class PhoneFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PhoneFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'


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
            'modified_date': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
            'note': forms.Textarea(attrs={'rows': 3}),}


class NoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NoteFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'
