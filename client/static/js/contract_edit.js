$(function(){
    setup_datepickers();
    setup_contract_tabs();
});

function setup_datepickers()
{
    var options = get_basic_date_picker_options();
    $("#id_contract-start_date").datepicker(options);
    $("#id_contract-referral_date").datepicker(options);
    $("#id_contract-end_date").datepicker(options);
}

function setup_contract_tabs()
{
    setup_contract_status();
    var tio_pane_elem = $('li.tab-pane a[href="#tio"]');
    if (tio_pane_elem.length > 0)
    {
        $('li.tab-pane:first').after(tio_pane_elem.parent());
    }
}

function setup_contract_status()
{
    $('#contract_status_table').appendTo('#status');
}