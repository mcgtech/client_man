$(function(){
    setup_datepickers();
    setup_contract_tabs();
    handle_page_readonly_state();
    setup_interview();
});

function setup_interview()
{
    $('#interview_block').appendTo('#interview');
    $('#edit_int').click(function(){
        var edit_url = data_from_django.edit_contract;
        window.location.href = edit_url;
    });
}

function handle_page_readonly_state()
{
    if (data_from_django.read_only)
    {
        make_page_read_only();
    }
}

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