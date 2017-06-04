$(function(){
    setup_interview_quals();
    setup_int_datepickers();
    setup_inline_add_listener();
});

function setup_inline_add_listener()
{
    // inline_add gets fired inside /static/js/form_helper/formset_manage.js
    $( document ).on( "inline_add", function( event, prefix, new_row ) {
        if (prefix == 'quals')
        {
            // add datepicker to new quals row date
            var options = get_basic_date_picker_options();
            $('input.datepicker', new_row).datepicker(options);
        }
    });
}

function setup_int_datepickers()
{
    var options = get_basic_date_picker_options();
    // int date
    $("#id_interview-interview_date").datepicker(options);
    // qualifications
    $("#qualifications .datepicker").datepicker(options);
}

function setup_interview_quals()
{
    // see #qualifications in interview_edit.html
    $('#qualifications').appendTo('#skillsqual');
    // attach formset handler
    setup_inline_quals();
}

var INLINE_QUALS_SETUP = false;
function setup_inline_quals()
{
    $('a[href="#skillsqual"]').parent().click(function(){
        if (!INLINE_QUALS_SETUP)
        {
             setTimeout(function(){
                $('#qualifications tbody tr').formset({prefix: 'quals'});
            }, 10);
            INLINE_QUALS_SETUP = true;
        }
    });
}