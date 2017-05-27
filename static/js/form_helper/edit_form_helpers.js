$(function(){
    setup_leave_form_check();
    request_conf_on_delete();
    manage_disabled_selects_in_a_form();
});

function setup_leave_form_check()
{
    // https://github.com/snikch/jquery.dirtyforms
    // does not work on safari at moment
    // in chrome on client edit it fires even if nothing changed - however am I using js to change stuff?
    // TODO: get this to work
    //$('form').dirtyForms({ ignoreSelector: 'select.ignore_dirty' });
}

function request_conf_on_delete()
{
    var delete_allowed = typeof data_from_django.delete_allowed !== 'undefined' ? data_from_django.delete_allowed : false;
    if (delete_allowed)
    {
        apply_confirm_to_submit_button('.delete-btn', 'btn-danger', 'del_butt', 'Delete', 'Deletion',
                                        'Are you sure that you want to delete this record?<br>This cannot be undone and it will delete any child records.');
    }
    else
    {
        $('.delete-btn').remove();
    }
}

// http://stackoverflow.com/questions/1191113/how-to-ensure-a-select-form-field-is-submitted-when-it-is-disabled
// if I don't do this then the data in the form elemetns that are disabled are not passed in the post, so it can
// result in data being lost on a save
function manage_disabled_selects_in_a_form()
{
    var save_pressed = false;
    $('#submit-id-save-record').click(function() {
          save_pressed = true;
    });
    $('form').bind('submit', function () {
        if (save_pressed)
        {
            $(this).find(':input').prop('disabled', false);
        }
    });
}