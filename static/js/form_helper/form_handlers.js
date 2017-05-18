// http://stackoverflow.com/questions/1191113/how-to-ensure-a-select-form-field-is-submitted-when-it-is-disabled
function manage_disabled_selects_in_a_form(form)
{
    form.bind('submit', function () {
    $(this).find(':input').prop('disabled', false);
    });
}