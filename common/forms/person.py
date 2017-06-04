from client.models import *
from common.models import Note, Address, Telephone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import *
from . import *
from django.conf import settings
# forms for editting


class AddressForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout('line_1', 'line_2', 'line_3',
                           Div(Div('post_code', css_class="col-sm-6"), css_class='row postcode'),
                           Div(Div('area', css_class="col-sm-6"), Div('evidence', css_class="col-sm-6"), css_class='row'),
                  )
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'line_3','post_code', 'area', 'evidence')
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

class NoteForm(AuditableForm):
    # helper = FormHelper()
    # helper.form_tag = False

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['modified_by'].widget.attrs['disabled'] = True
    #     self.fields['modified_date'].widget.attrs['disabled'] = True
    #     # self.helper.form_tag = True
    class Meta(AuditableForm.Meta):
        AuditableForm.Meta.model = Note
        fields = ('note', ) + get_auditable_fields()
        AuditableForm.Meta.widgets['note'] = forms.Textarea(attrs={'rows': 3, 'cols': 100})
    # class Meta:
    #     model = Note
    #     fields = ('note', 'modified_by', 'modified_date', )
    #     widgets = {
    #         'modified_date': forms.DateInput(format=(settings.DISPLAY_DATE_TIME)),
    #         'note': forms.Textarea(attrs={'rows': 3}),}


class NoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NoteFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_tag = False
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'
