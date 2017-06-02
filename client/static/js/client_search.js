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
                handle_print_action_selection(1);
                break;
            case '2':
                handle_print_action_selection(2);
                break;
        }
    });
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