$(function(){
    setup_client_form();
    setup_client_phones();
    setup_client_address();
    setup_client_notes();
    setup_datepickers();
    setup_leave_form_check();
});

function setup_leave_form_check()
{
    // does not work on safari at moment
    $('form').dirtyForms();
}

function setup_client_form()
{
    // move age
    var age = $('#client_age').html();
    var age_markup = '<div class="col-sm-4"><label for="id_main-birth_certificate" class="control-label ">Age</label>' + age + '</div>';
    $('.dob').append(age_markup);
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
    setup_form_datepicker($("#id_main-dob"), new Date('January 1, 1990'), null);
}

function setup_end_date_datepicker()
{
    setup_form_datepicker($("#id_main-end_date"), new Date(), new Date());
}

function setup_datepickers()
{
    setup_dob_datepicker();
    setup_end_date_datepicker();
}

function setup_form_datepicker(elem, start_date, minDate)
{
    var options = {
          changeMonth: true,
          changeYear: true,
          yearRange: start_date.getFullYear() + ':' + new Date().getFullYear(),
          defaultDate: start_date,
          dateFormat: 'dd/mm/yy'
        }
    if (minDate != null)
    {
        options.minDate = minDate;
    }
    elem.datepicker(options);
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
