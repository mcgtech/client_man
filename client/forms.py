from django import forms
from .models import Client, Note, Address
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Button, Div, Field
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, InlineField
from common.forms import validate_form_fields, validate_required_field
#
# class NoFormTagCrispyFormMixin(object):
#     @property
#     def helper(self):
#         if not hasattr(self, '_helper'):
#             self._helper = FormHelper()
#             self._helper.form_tag = False
#         return self._helper


# had to use helper as shown in https://blog.bixly.com/awesome-forms-django-crispy-forms
# otherwise tabs doesn't work
class ClientForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Main',
                'title',
                'sex',
                'first_name',
                'middle_name',
                'last_name',
                'known_as',
                'dob',
                'birth_certificate',
                'marital_status',
                'ethnicity'
            ),
            Tab(
                'Project',
                'type',
                'social_work_involved'
            )
        )
    )
    helper.form_tag = False
    helper.add_input(Submit("save client", "Save"))
    helper.add_input(Submit("delete client", "Delete", css_class='btn btn-danger'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['first_name'].label = "First Name*"
        self.fields['last_name'].label = "Last Name*"
        self.fields['dob'].label = "Date of Birth*"

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_first_name(self):
        return validate_required_field(self, 'first_name', 'first name')

    def clean_last_name(self):
        return validate_required_field(self, 'last_name', 'last name')

    def clean_dob(self):
        return validate_required_field(self, 'dob', 'date of birth')

    # display error at page level for errors generated during required field validation
    def clean(self):
        return validate_form_fields(self)

    class Meta:
        model = Client
        fields = ('title', 'first_name', 'middle_name', 'last_name', 'known_as', 'dob', 'sex',
                  'birth_certificate', 'ethnicity', 'type', 'social_work_involved', 'marital_status')
        widgets = {
            'dob': forms.DateInput(attrs={'class':'datepicker'}),}


class AddressForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'line_3', 'post_code', 'area', 'evidence')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # the following is to allow control of field required validation at page and field level
        self.form_errors = []
        self.fields['line_1'].label = "Address line 1*"

    # if I make the following field required in the model, then as I am using tabs, the default form validation for
    # required fields in crispy forms for bootstrap shows a popover against the offending field when save is clicked
    # and if that tab is not on display then the user will not see the error, hence I took the following approach:
    # validate required fields and display error at field level
    def clean_line_1(self):
        return validate_required_field(self, 'line_1', 'line 1')

    # display error at page level for errors generated during required field validation
    def clean(self):
        return validate_form_fields(self)

class NoteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
            'note',
            InlineField('modified_by', readonly=True),
            InlineField('modified_date', readonly=True)
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['modified_by'].widget.attrs['disabled'] = True
        self.fields['modified_date'].widget.attrs['disabled'] = True

        self.helper.form_tag = True
    class Meta:
        model = Note
        fields = ('note', 'modified_by', 'modified_date', )



class NoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(NoteFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.template = 'bootstrap/table_inline_formset.html'












class ClientWorksForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Basic Information',
                'title',
                'first_name',
                'middle_name',
                'last_name',
                'known_as'
            ),
            Tab(
                'Contact',
                'dob',
                'sex'
            )
        )
    )
    #helper.form_method = 'POST'
    #helper.add_input(Submit('login', 'login', css_class='btn-primary'))
    class Meta:
        model = Client
        fields = ('title', 'first_name', 'middle_name', 'last_name', 'known_as', 'dob', 'sex')
        widgets = {
            'dob': forms.DateInput(attrs={'class':'datepicker'}),}

class NoteWorksForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('note', 'modified_by', 'modified_date', )


class ExampleForm(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab(
                'Basic Information',
                'like_website',
                'favorite_food'
            ),
            Tab(
                'Address',
                'favorite_color',
                'favorite_number',
                'notes'
            )
        )
    )

class ExampleFormDoesntShowTabs(forms.Form):
    like_website = forms.TypedChoiceField(
        label = "Do you like this website?",
        choices = ((1, "Yes"), (0, "No")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,
    )

    favorite_food = forms.CharField(
        label = "What is your favorite food?",
        max_length = 80,
        required = True,
    )

    favorite_color = forms.CharField(
        label = "What is your favorite color?",
        max_length = 80,
        required = True,
    )

    favorite_number = forms.IntegerField(
        label = "Favorite number",
        required = False,
    )

    notes = forms.CharField(
        label = "Additional notes or feedback",
        required = False,
    )
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_method = 'post'
        TabHolder(
            Tab('First Tab',
                'like_website',
                Div('favorite_food')
                ),
            Tab('Second Tab',
                Field('favorite_color', css_class="extra")
                )
        )

class ExampleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_method = 'post'
        self.layout = Layout(
            'favorite_color',
            'favorite_food',
        )
        self.render_required_fields = True
        self.helper.form_tag = False