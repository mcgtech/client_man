
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from .models import EmailTemplate
from common.forms import *

class EmailTemplateForm(AuditableForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Main',
                    Div(Div('template_identifier', css_class="col-sm-6"), Div('subject', css_class="col-sm-6"), css_class='row'),
                    Div(Div('from_address', css_class="col-sm-6"), Div('to_addresses', css_class="col-sm-6"), css_class='row'),
                    Div(Div('cc_addresses', css_class="col-sm-6"), Div('bcc_addresses', css_class="col-sm-6"), css_class='row'),
                    'plain_body', 'html_body'),
                Tab(
                    'Log',
                    'created_by',
                    'created_on',
                    'modified_by',
                    'modified_on'
                )))

    class Meta(AuditableForm.Meta):
        model = EmailTemplate
        fields = get_auditable_fields() + ('template_identifier', 'subject', 'from_address', 'to_addresses', 'cc_addresses', 'bcc_addresses', 'plain_body', 'html_body')
        AuditableForm.Meta.widgets['to_addresses'] = forms.Textarea(attrs={'rows':2})
        AuditableForm.Meta.widgets['cc_addresses'] = forms.Textarea(attrs={'rows':2})
        AuditableForm.Meta.widgets['bcc_addresses'] = forms.Textarea(attrs={'rows':2})