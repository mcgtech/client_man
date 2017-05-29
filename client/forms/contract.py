from django import forms
from client.models import Contract, TIOContract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import *
from django.conf import settings

# forms for editting

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class ContractForm(AuditableForm):
    def __init__(self, *args, **kwargs):
        add_contract = kwargs.pop('add_contract')
        super().__init__(*args, **kwargs)
        if add_contract:
            self.helper.add_input(Button("add contract", "Add New Contract", css_class='btn btn-success add-contract-btn', data_toggle="modal", data_target="#contract_select_modal"))
        self.prepare_required_field('type', 'Type')
        self.prepare_required_field('start_date', 'Start date')
        self.fields['type'].widget.attrs['readonly'] = True
        self.fields['secondary_client_group'].required = False # not sure why I had to do this as its defined in model as not required
        self.helper.layout = Layout(
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
                    'Status',
                ),
                    Tab(
                        'Log',
                        'created_by',
                        'created_on',
                        'modified_by',
                        'modified_on'
                    )))

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
        fields = get_auditable_fields() + ('type', 'secondary_client_group', 'start_date', 'end_date', 'referral_date',
                                            'secondary_client_group_evidence', 'application_form')
        AuditableForm.Meta.widgets['start_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['end_date'] = forms.DateInput(attrs={'class':'datepicker'})
        AuditableForm.Meta.widgets['referral_date'] = forms.DateInput(attrs={'class':'datepicker'})


class TIOContractForm(ContractForm):
    class Meta(ContractForm.Meta):
        model = TIOContract
        ContractForm.Meta.fields = ContractForm.Meta.fields + ('issue', 'consent_form_complete', 'aa_progress_jsa_18',
                                                               'add_support_jsa_18', 'add_support_jsa_25', 'wca_incapacity',
                                                               'support_esa', 'wrag_esa', 'emp_pros_inc', 'other_ben',
                                                               'fund_mgr_notes', 'partner', 'closed_date')
        AuditableForm.Meta.widgets['closed_date'] = forms.DateInput(attrs={'class':'datepicker'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prepare_required_field('issue', 'Adult 18+ with')
        # http://django-crispy-forms.readthedocs.io/en/d-0/dynamic_layouts.html
        self.helper.layout[0].append(Tab(
                        'TIO',
                        Div(
                Div('partner', 'issue',
                    'consent_form_complete', 'closed_date',
                    Fieldset('JSA claimants 18-24 (less than 9 months)', 'aa_progress_jsa_18', 'add_support_jsa_18', css_class="con_field"),
                    Fieldset('JSA claimants over 25 (less than 12 months)', 'add_support_jsa_25', css_class="con_field"),
                    Fieldset('Incapacity Benefit', 'wca_incapacity', css_class="con_field"),
                    Fieldset('ESA', 'support_esa', 'wrag_esa', css_class="con_field"),
                    Fieldset('Income Support', 'emp_pros_inc', css_class="con_field"),
                    css_class="col-sm-6"),
                Div('other_ben', 'fund_mgr_notes',
                    css_class="col-sm-6"),
                css_class="row tio")))

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_issue(self):
        return validate_required_field(self, 'issue', 'Adult 18+ with')