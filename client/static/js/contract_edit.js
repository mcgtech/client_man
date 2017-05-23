$(function(){
    setup_datepickers();
});

function setup_datepickers()
{
    var options = get_basic_date_picker_options();
    $("#id_contract-start_date").datepicker(options);
    $("#id_contract-referral_date").datepicker(options);
    $("#id_contract-end_date").datepicker(options);
}
