from client.models import *
from common.models import Note, Address, Telephone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import *
from django.conf import settings

# forms for editting

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class ClientForm(EditForm, AuditableForm):
    username = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        add_contract = kwargs.pop('add_contract')
        super().__init__(*args, **kwargs)
        if add_contract:
            self.helper.add_input(Button("add contract", "Add New Contract", css_class='btn btn-success add-contract-btn', data_toggle="modal", data_target="#contract_select_modal"))
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Main',
                    Div('title', 'forename', 'middle_name', 'surname', 'known_as', 'sex',
                        css_class="col-sm-6"),
                    Div(
                        # age is added directly in the template and manipulated via js
                        Div(Div('dob', css_class="col-sm-4"), Div('birth_certificate', css_class="col-sm-4"),
                            css_class='row dob'),
                        'marital_status', 'ethnicity',
                        'created_by', 'created_on', 'modified_by', 'modified_on',
                        css_class="col-sm-6")
                ),
                Tab(
                    'Project',
                    Div(
                        'client_status',
                        Div(Div('start_date', css_class="col-sm-6"), Div('end_date', css_class="col-sm-6"),
                            css_class='row'),
                        'nat_ins_number', 'education', 'jsa', 'recommended_by', 'social_work_involved',
                        css_class="col-sm-6"),
                    Div(
                        Div(Div('client_group', css_class="col-sm-6"),
                            Div('client_group_evidence', css_class="col-sm-6"), css_class='row evid'),
                        Div(Div('employment_status', css_class="col-sm-6"),
                            Div('employment_status_evidence', css_class="col-sm-6"), css_class='row emp_state'),
                        'time_unemployed', 'stage', 'ref_received',
                        css_class="col-sm-6")
                ),
                Tab(
                    'Contracts',
                ),
                Tab(
                    'User',
                    'email_address',
                    'username',
                    'password'
                )
            )
        )

        self.prepare_required_field('title', 'Title')
        self.prepare_required_field('client_status', 'Client status')
        self.prepare_required_field('forename', 'First Name')
        self.prepare_required_field('surname', 'Last Name')
        self.prepare_required_field('dob', 'Date of birth')
        self.prepare_required_field('recommended_by', 'Recommended by')
        self.prepare_required_field('jsa', 'JSA')
        self.prepare_required_field('education', 'Education')
        self.prepare_required_field('client_group', 'Client group')
        self.prepare_required_field('time_unemployed', 'Time unemployed')
        self.prepare_required_field('sex', 'Sex')
        self.prepare_required_field('marital_status', 'Marital status')
        self.prepare_required_field('ethnicity', 'Ethnicity')

        self.fields['education'].error_messages = {'required': 'Education is required'}
        self.fields['start_date'].widget.attrs['readonly'] = True

        self.fields['employment_status'].required = False
        self.fields['stage'].required = False


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

    def clean_email_address(self):
        email = self.cleaned_data['email_address']
        if email and not is_email_valid(email):
            error_msg = 'email address is not valid'
            self.form_errors.append(error_msg)
            raise forms.ValidationError(error_msg)
        return email

    class Meta(AuditableForm.Meta):
        AuditableForm.Meta.model = Client
        fields = get_auditable_fields() + ('title', 'forename', 'middle_name', 'surname',
                                           'known_as', 'dob', 'sex', 'email_address',
                                           'birth_certificate', 'ethnicity', 'social_work_involved', 'marital_status',
                                           'employment_status_evidence', 'start_date', 'end_date', 'nat_ins_number',
                                           'education', 'recommended_by', 'jsa', 'employment_status',
                                           'time_unemployed', 'stage', 'client_group', 'ref_received',
                                           'client_group_evidence', 'client_status')
        AuditableForm.Meta.widgets['dob'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['start_date'] = forms.DateInput(format=(settings.DISPLAY_DATE))
        AuditableForm.Meta.widgets['end_date'] = forms.DateInput(format=(settings.DISPLAY_DATE), attrs={'class':'datepicker'})