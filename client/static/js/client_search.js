$(function(){
    setup_client_search();
});

function setup_client_search()
{
    $('th.selection input').change(function(){
        var state = $(this).is(':checked');
        $('td.selection input').prop('checked', state);
    });
}
