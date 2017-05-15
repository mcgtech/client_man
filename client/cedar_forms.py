from django import forms
from django.forms.fields import ChoiceField, BooleanField
from django_select2.forms import ModelSelect2MultipleWidget

from crispy_forms_pure.forms import PureModelForm, PureForm
from crispy_forms_pure.layout import Layout, Fieldset, Field, Div

from autocomplete_light.fields import ModelChoiceField
from autocomplete_light.widgets import TextWidget

from .models import Job

from django.conf import settings

class JobSearchForm(forms.Form):
    """ JobSearchForm(data, **kwargs)
        Search form for client instances
    """

    q = forms.CharField(
        widget=TextWidget(autocomplete='JobAutocomplete', attrs={'type': 'search', 'placeholder': 'Search'}),
        required=False
    )


class StaffSelect2Widget(ModelSelect2MultipleWidget):
    search_fields = [
        'account_name__icontains',
    ]

class BaseJobForm(PureModelForm):
    classes = 'pure-form pure-form-aligned fix-input-widths'
    switches = False

    class Meta:
        model = Job
        exclude = ('job_id', 'last_review_details',)
        widgets = {
            'staff_to_allocate_time': StaffSelect2Widget,
        }


    MINIMAL_FIELDS = (
        'client',
        'billing_address',
        'property_name',
        'job_type',
        'CKDG_job_code',
        'job_partner',
        'job_manager',
        'primary_office',
        'primary_business_stream',
        'openair_project_template',
        'pi_category',
        'pi_geography',
        'fee_structure'
    )

    LENDING_FIELDS = (
        'buy_to_let',
        'new_build',
        'who_is_lender',
        'miles_from_office',
        'rbg_pav_number',
        'rbg_address_of_property',
        'rbg_date_of_valuation',
        'rbg_branch_address_of_bank_contact',
    )

    UA_FIELDS = (
        'CKDG_job_code',
        'fieldsman',
    )


    layout = Layout(
        Fieldset(
            'Client Information',
            'client',
            'address_hidden_field',
            Div(
              id='ajax_addresses',
            ),
            Div(
                'address_name',
                'address_street',
                'address_city',
                'address_state',
                'address_country',
                'address_postcode',
                id='new_address',
            )
        ),

        Fieldset(
            'Primary Information',
            'job_type',
            Div(
              'is_sale',
              id='sale_boolean',
              style='display: none'
            ),
            Div(
                'property_name',
                'internet_charge',
                id='property_name',
                style='display:none'
            ),
            Div(
                'job_name',
                id='job_name',
            ),
            'is_united_auctions_job',
            Div(
                'CKDG_job_code',
                'fieldsman',
                id='ua-details',
                style='display: none'
            ),
            'job_partner',
            'job_manager',
            'primary_office',
            'primary_business_stream'
        ),

        Fieldset(
            'Lending specific details',
            Div(
                'buy_to_let',
                'new_build',
                'who_is_lender',
                Div(
                  'other_lender',
                  id='other_lender',
                  style='display: none'
                ),
                'miles_from_office',
                Div(
                    'rbg_pav_number',
                    'rbg_address_of_property',
                    'rbg_date_of_valuation',
                    'rbg_branch_address_of_bank_contact',
                    id='rbg-details',
                    style='display: none'
                ),
                id='lending-details',
                style='display: none'
            )
        ),

        Fieldset(
            'Job Management',
            'job_number',
            'openair_project_template',
            'pi_category',
            'pi_geography',
            'fee_structure',
            Div(
                'fixed_fee_amount',
                id='fixed-fee',
                style='display: none'
            ),
            Div(
                'percentage',
                'percentage_of',
                id='percentage-fee',
                style='display: none'
            ),
            'third_party_fee',
            'expenses_to_be_charged',
            'admin_percentage',
            'commission_due',
            Div(
                'commission_due_to',
                id='commission_due_to',
                style='display:none'
            ),
            'source_of_business',
            'staff_to_allocate_time',
            'need_reviewing',
            Div(
                'created_by',
                style='display:none;'
            )
        )
    )


    address_name = forms.CharField(max_length=100, required=False)
    address_street = forms.CharField(max_length=100, required=False, label="Address Line 1")
    address_city = forms.CharField(max_length=100, required=False, label="Address Line 2")
    address_state = forms.CharField(max_length=100, required=False, label="Address Line 3")
    address_country = forms.CharField(max_length=100, required=False, label="Address Line 4")
    address_postcode = forms.CharField(max_length=100, required=False, label="Postcode")
    address_hidden_field = forms.CharField(max_length="200", widget=forms.HiddenInput, required=False)
    is_united_auctions_job = BooleanField(required=False)


    client = ModelChoiceField(
        autocomplete='ClientAutocomplete',
        help_text='Use this field to select which client should be used. If you cannot find the client, you'
                  'need to create it first.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.data and 'is_lending_job' not in self.data:
            for field in self.LENDING_FIELDS:
                self.fields.get(field).required = False

        if self.data and 'is_united_auctions_job' not in self.data:
            for field in self.UA_FIELDS:
                self.fields.get(field).required = False

        self.fields['created_by'].widget.attrs['readonly'] = True

        self.helper.form_tag = True



    def clean_client(self):
        client = self.cleaned_data['client']

        if client.status == "Drafted" or client.status == "Rejected":
            self.add_error('client', "Please select a client whose status is not Drafted or Rejected")

        return client


    def clean_admin_percentage(self):
        admin_percentage = self.cleaned_data['admin_percentage']

        if admin_percentage and admin_percentage < 0:
            self.add_error('admin_percentage', "Please enter a percentage > 0%.")

    def clean(self):

        cleaned_data = super(BaseJobForm, self).clean()

        #clean lender data-ensure rvg feilds are all filled out where necessary.
        lender = cleaned_data.get('who_is_lender')
        other_lender = cleaned_data.get('other_lender')
        pav_number = cleaned_data.get('rbg_pav_number')
        rbg_address = cleaned_data.get('rbg_address_of_property')
        rbg_valuation = cleaned_data.get('rbg_date_of_valuation')
        rbg_branch_address = cleaned_data.get('rbg_branch_address_of_bank_contact')

        if lender == "Royal Bank Group":

            if not pav_number or not rbg_address or not rbg_valuation or not rbg_branch_address:
                raise forms.ValidationError("All RBG information must be completed.")

        #clean fee structure data so that relevant fields are filled out

        is_sale = cleaned_data.get('is_sale')
        job_type = cleaned_data.get('job_type')
        property_name = cleaned_data.get('property_name')
        job_name = cleaned_data.get('job_name')

        if job_type == 'valuation_non_valuation':
            if not is_sale:
                self.add_error('is_sale', 'This field is required.')

            if is_sale == 'Yes' and not property_name:
                self.add_error('property_name', 'This field is required.')

            if is_sale == 'No' and not job_name:
                self.add_error('job_name', 'This field is required.')

        if job_type == 'valuation_lending' and not other_lender:
            self.add_error('other_lender', 'This field is required.')

        percentage = cleaned_data.get('percentage')
        fee_structure = cleaned_data.get('fee_structure')

        if fee_structure == "Percentage":
            if not percentage:
                self.add_error('percentage', "This field is required.")
            elif percentage and percentage < 0:
                self.add_error('percentage', "Please enter a percentage > 0%.")


        #clean address so fields are required if there hasn't been an existing address entered.

        name = cleaned_data.get('address_name')
        street = cleaned_data.get('address_street')
        city = cleaned_data.get('address_city')
        postcode = cleaned_data.get('address_postcode')
        pi_category = cleaned_data.get('pi_category')

        if job_type == "valuation_lending":
            if pi_category:
                if not pi_category[:3] == "LEN":
                    self.add_error('pi_category', 'Pi category must begin with "LEN" for lending jobs.')


        address_id = cleaned_data.get('address_hidden_field')
        if not address_id:
            if not name or not street or not postcode:
                raise forms.ValidationError("Please select an existing address, or enter a new one. Name, Address Line 1 and Postcode are required.")

        return cleaned_data


class ReviewForm(forms.Form):
    notes_field = forms.CharField(max_length="5000", label="Reason for action", widget=forms.Textarea(attrs={'rows': 15, 'cols': 125}), required=False)
    netsuite_id = forms.CharField(max_length=20, label="Netsuite ID", required=False)
    hidden_field = forms.CharField(max_length="200", widget=forms.HiddenInput)

