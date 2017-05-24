from django import forms
from client.models import Contract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import *
from django.conf import settings

# forms for editting

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class ContractForm(AuditableForm):
    helper = FormHelper()
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Main',
                Div(
        Div('type',
            'start_date',
            'end_date',
            'referral_date',
            css_class="col-sm-6"),
        Div('secondary_client_group', 'secondary_client_group_evidence',
            'application_form',
            css_class="col-sm-6"),
        css_class="row")),
            Tab(
                'Log',
                'created_by',
                'created_on',
                'modified_by',
                'modified_on'
            )))
    helper.form_tag = False
    helper.add_input(Submit("save contract", "Save"))
    helper.add_input(Submit("delete contract", "Delete", css_class='btn btn-danger delete-btn'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepare_required_field('type', 'Type')
        self.prepare_required_field('start_date', 'Start date')

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_type(self):
        return validate_required_field(self, 'type', 'type')

    def clean_start_date(self):
        return validate_required_field(self, 'start_date', 'start date')

    class Meta(AuditableForm.Meta):
        model = Contract
        fields = get_auditable_fields()  + ('type', 'secondary_client_group', 'start_date', 'end_date', 'referral_date',
                                            'secondary_client_group_evidence', 'application_form')
        AuditableForm.Meta.widgets['start_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['end_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['referral_date'] = forms.DateInput(attrs={'class':'datepicker'})

