$(function(){
    setup_leave_form_check();
    request_conf_on_delete();
});
function setup_leave_form_check()
{
    // does not work on safari at moment
    $('form').dirtyForms();
}

function request_conf_on_delete()
{
    apply_confirm_to_submit_button('.delete-btn', 'btn-danger', 'del_butt', 'Delete', 'Deletion',
                                    'Are you sure that you want to delete this record?<br>This cannot be undone and it will delete any child records.');
}