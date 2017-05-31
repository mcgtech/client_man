$(function(){
    setup_client_search();
    setup_list_action_handler_handler();
});

function setup_client_search()
{
    $('th.selection input').change(function(){
        var state = $(this).is(':checked');
        $('td.selection input').prop('checked', state);
    });
}

function setup_list_action_handler_handler()
{
    $('#execute_action').click(function(){
        var sel = $('#id_actions').val();
        switch (sel)
        {
            case '0':
                bootbox.alert('Please select an action');
                break;
            case '1':
                handle_delete_action_selection();
                break;
            case '2':
                handle_print_action_selection(1);
                break;
            case '2':
                handle_print_action_selection(2);
                break;
        }
    });
}

function handle_delete_action_selection()
{
    bootbox.confirm('Are you sure that you want to delete the selected itm(s)?', delete_the_items);
}

function delete_the_items(ok_selected)
{
    if (ok_selected)
    {
        var id_selector = function() { return $(this).val(); };
        var entity_ids = $('tr td.selection input:checked').map(id_selector).get();
        if (entity_ids.length == 0)
        {
            bootbox.alert('Please select at least one item');
        }
        else
        {
            alert('still to code');
        }
    }
}

function handle_print_action_selection(report_id)
{
    var id_selector = function() { return $(this).val(); };
    var entity_ids = $('tr td.selection input:checked').map(id_selector).get();
    if (entity_ids.length == 0)
    {
        bootbox.alert('Please select at least one item');
    }
    else
    {
        populate_print_area(entity_ids, report_id);
    }
}

function request_conf_on_delete_in_form_edit()
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