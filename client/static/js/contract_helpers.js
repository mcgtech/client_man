$(function(){
    setup_contract_handlers();
});

function setup_contract_handlers()
{
    $('#button-id-add-contract').click(function(){
        window.location.href = data_from_django.add_con_url;
    });
}
