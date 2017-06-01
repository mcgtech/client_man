from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.models import HTMLTemplate
from common.forms import *

class HTMLTemplateForm(AuditableForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(Div(Div('template_identifier', css_class="col-sm-6"), Div('type', css_class="col-sm-6"), css_class='row'), 'body')
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Main',
                    Div(Div('template_identifier', css_class="col-sm-6"), Div('type', css_class="col-sm-6"),
                        css_class='row'), 'body'),
                Tab(
                    'Log',
                    'created_by',
                    'created_on',
                    'modified_by',
                    'modified_on'
                )))

    class Meta(AuditableForm.Meta):
        model = HTMLTemplate
        fields = get_auditable_fields() + ('template_identifier', 'type', 'body')