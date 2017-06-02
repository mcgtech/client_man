
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from .models import ReportTemplate
from common.forms import *

class ReportTemplateForm(AuditableForm, EditForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Main',
                    'template_identifier', 'body'),
                Tab(
                    'Tags',
                ),
                Tab(
                    'Log',
                    'created_by',
                    'created_on',
                    'modified_by',
                    'modified_on'
                )))

    class Meta(AuditableForm.Meta):
        model = ReportTemplate
        fields = get_auditable_fields() + ('template_identifier', 'body')
        AuditableForm.Meta.widgets['body'] = forms.Textarea(attrs={'rows':20})