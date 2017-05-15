from django import forms


def validate_form_fields(self):
    if (len(self.form_errors) > 0):
        errors = ", ".join(self.form_errors)
        raise forms.ValidationError(errors)
    else:
        return self.cleaned_data  # never forget this! ;o)

def validate_required_field(self, field_name, field_name_desc):
    fld = self.cleaned_data[field_name]
    if not fld:
        error_msg = field_name_desc + " cannot be empty"
        self.form_errors.append(error_msg)
        raise forms.ValidationError(error_msg)
    return fld