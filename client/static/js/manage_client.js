$(function(){
    setup_client_form();
    setup_client_address();
    setup_client_notes();
    setup_dob_datepicker();
});

function setup_client_form()
{
    manage_disabled_selects_in_a_form($('#client_edit_form'));
    apply_confirm_to_submit_button('#submit-id-delete-client', 'btn-danger', 'del_butt', 'Delete', 'Deletion',
                                    'Are you sure that you want to delete this client?');
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

function setup_client_address()
{
    // crispy-forms handle one to one, so I handle the one to many elems here - ie move into a separate tab
    // see #notes in client_edit.html
    $('.tab-pane:first').after('<li class="tab-pane"><a href="#address" data-toggle="tab">Address</a></li>');
    $('#address').appendTo('.tab-content');
}

function setup_dob_datepicker()
{
    var start_year = '1990';
    var start_date = new Date('January 1, ' + start_year);
    $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true,
      yearRange: start_year + ':' + new Date().getFullYear(),
      defaultDate: start_date,
      dateFormat: 'dd/mm/yy'
    });
}

function setup_inline_client_notes()
{
    $('#client_notes').click(function(){
//        setTimeout(function(){
//            $('#notes tbody tr').formset({prefix: 'nested'});
//        }, 10);

            $('#notes tbody tr').formset({prefix: 'nested'});
        });
}
