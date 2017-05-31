$(function(){
    setup_client_search();
    setup_print_handler();
});

function setup_client_search()
{
    $('th.selection input').change(function(){
        var state = $(this).is(':checked');
        $('td.selection input').prop('checked', state);
    });
}

function setup_print_handler()
{
    $('#execute_action').click(function(){
        var sel = $('#id_actions').val();
        switch (sel)
        {
            case '0':
                bootbox.alert('Please select an action');
                break;
            case '1':
                var id_selector = function() { return $(this).val(); };
                var client_ids = $('tr td.selection input:checked').map(id_selector).get();
                if (client_ids.length == 0)
                {
                    bootbox.alert('Please select at least one client');
                }
                else
                {
                    populate_print_area(client_ids, 1);
                }
                break;
        }
    });
}