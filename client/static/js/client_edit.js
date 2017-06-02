$(function(){
    setup_client_form();
    setup_client_phones();
    setup_client_address();
    setup_client_contracts();
    setup_client_notes();
    setup_datepickers();
    add_printing();
    handle_page_readonly_state();
});

function handle_page_readonly_state()
{
    if (data_from_django.read_only)
    {
        make_page_read_only();
        disable_old_links($('#contracts a'));
    }
}

function add_printing()
{
    $('#print-client').click(function(){
        print_report(1);
    });
    $('#print-con').click(function(){
        print_report(2);
    });
}

function print_report(report_id)
{
    var client_id = get_client_id();
    if (client_id === null)
    {
        bootbox.alert('Press save first.');
    }
    else
    {
        populate_print_area([client_id], report_id);
    }
}


function get_client_id()
{
    return typeof data_from_django.client_id != 'undefined' ? data_from_django.client_id : null;
}

function setup_client_form()
{
    // move age
    var age = $('#client_age').html();
    var age_markup = '<div class="col-sm-4"><label for="id_main-birth_certificate" class="control-label ">Age</label>' + age + '</div>';
    $('.dob').append(age_markup);
}

function setup_client_contracts()
{
    $('#contracts_table').appendTo('#contracts');
}

function setup_client_notes()
{
    // crispy-forms handle one to one, so I handle the one to many elems here - ie move into a separate tab
    // see #notes in client_edit.html
    $('.nav-tabs').append('<li id="client_notes" class="tab-pane"><a href="#notes" data-toggle="tab">Notes</a></li>');
    $('#notes').appendTo('.tab-content');
    // attach formset handler
    setup_inline_client_notes();
}

function setup_client_phones()
{
    var phones_elem = $('#phones');
    phones_elem.prepend('<label for="id_main-middle_name" class="control-label ">Phones</label>');
    phones_elem.appendTo('#main > div:first');
    // attach formset handler
    setup_inline_client_phones();
}

function setup_client_address()
{
    // crispy-forms handle one to one, so I handle the one to many elems here - ie move into a separate tab
    // see #notes in client_edit.html
    $('.tab-pane:first').after('<li class="tab-pane"><a href="#address" data-toggle="tab">Address</a></li>');
    $('#address').appendTo('.tab-content');
}

function setup_dob_datepicker()
{
    var options = get_basic_date_picker_options();
    options.defaultDate = new Date('January 1, 1990');

    $("#id_main-dob").datepicker(options);
}

function setup_end_date_datepicker()
{
    var options = get_basic_date_picker_options();

    $("#id_main-end_date").datepicker(options);
}

function setup_datepickers()
{
    setup_dob_datepicker();
    setup_end_date_datepicker();
}

function setup_inline_client_notes()
{
    $('#client_notes').click(function(){
        setTimeout(function(){
            $('#notes tbody tr').formset({prefix: 'nested'});
        }, 10); });
}

function setup_inline_client_phones()
{
    setTimeout(function(){
            $('#phones tbody tr').formset({prefix: 'phones'});
        }, 10);
}
