$(function(){
    setup_contract_handlers();
});

function setup_contract_handlers()
{
    $('#con-types').change(function(){
        var con_type_id = $('#con-types').val();
        window.location.href = data_from_django.add_con_url + con_type_id + '/';
    });
}