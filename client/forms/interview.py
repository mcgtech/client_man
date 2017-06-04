from django import forms
from client.models import Interview, Qualification, PlannedTraining
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import *
# forms for editing

# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class InterviewForm(EditForm, AuditableForm):
    def __init__(self, *args, **kwargs):
        add_int = kwargs.pop('add_interview')
        super().__init__(*args, **kwargs)
        if add_int:
            self.helper.add_input(Button("add interview", "Add New Interview", css_class='btn btn-success add-contract-btn', data_toggle="modal", data_target="#interview_select_modal"))
        self.helper.layout = Layout(
                TabHolder(
                    Tab('Main',
                        Div(Div('interviewer', css_class="col-sm-6"), Div('interview_date', css_class="col-sm-6"), css_class="row"), 'background_info',
                        'pref_job_dir', 'prev_work_exp', 'other_comments', 'scanned_copy'),
                    Tab('Skills/Qual',
                        Div('skills'), css_class="skills"),
                    Tab('Issues',
                        Div('dev_issues')),
                    Tab('Agencies',),
                    Tab(
                        'Log',
                        'created_by',
                        'created_on',
                        'modified_by',
                        'modified_on'
                    )))


    class Meta(AuditableForm.Meta):
        model = Interview
        fields = get_auditable_fields() + ('interviewer', 'interview_date', 'dev_issues', 'pref_job_dir', 'background_info', 'prev_work_exp', 'skills', 'dev_issues', 'other_comments', 'scanned_copy',)
        AuditableForm.Meta.widgets['interview_date'] = forms.DateInput(attrs={'class':'datepicker'})


class QualificationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = Qualification
        fields = ('title', 'level', 'grade', 'date_achieved', )
        widgets = {
            'date_achieved': forms.DateInput(format=(settings.DISPLAY_DATE), attrs={'class':'datepicker'}),}

class QualificationFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(QualificationFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'


class LearningForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = Learning
        fields = ('learning',)

class LearningFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LearningFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'


class PlannedTrainingForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = PlannedTraining
        fields = ('training',)

class PlannedTrainingFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlannedTrainingFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'


class OtherAgenciesForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = OtherAgencies
        fields = ('agency', 'contact_person', 'contact_details')

class OtherAgenciesFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OtherAgenciesFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'


class OtherProgrammesForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = OtherProgrammes
        fields = ('programme', 'provider', 'end_date')
        widgets = {
            'end_date': forms.DateInput(format=(settings.DISPLAY_DATE), attrs={'class':'datepicker'}),}

class OtherProgrammesFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(OtherProgrammesFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_tag = False
        self.template = 'bootstrap3/table_inline_formset.html'