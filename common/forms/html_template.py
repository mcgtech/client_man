from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from common.models import HTMLTemplate

class HTMLTemplateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(Div(Div('type', css_class="col-sm-6"), Div('title', css_class="col-sm-6"), css_class='row'), 'body')
    class Meta:
        model = HTMLTemplate
        fields = ('type', 'title', 'body')