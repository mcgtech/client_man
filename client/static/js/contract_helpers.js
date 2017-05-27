$(function(){
    setup_contract_handlers();
});

function setup_contract_handlers()
{
    $('#button-id-add-contract').click(function(){
        $('#contract_select').show();
    });

    $('#con-cancel').click(function(){
        $('#contract_select').hide();
    });

    $('#con-types').change(function(){
        var create_button = $('#con-create');
        if ($(this).val() == 'None')
        {
            create_button.prop('disabled', true);
        }
        else
        {
            create_button.removeAttr('disabled');
        }
    });

    $('#con-create').click(function(){
        $('#contract_select').hide();
        var con_type_id = $('#con-types').val();
        window.location.href = data_from_django.add_con_url + con_type_id + '/';
    });
}