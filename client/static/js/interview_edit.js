$(function(){
    setup_interview_formsets();
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
            apply_datepicker_on_add_event('qualifications', options)
        }
        if (prefix == 'other_progs')
        {
            // add datepicker to new other progs row date
            var options = get_basic_date_picker_options();
            apply_datepicker_on_add_event('other_progs', options)
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
    // other progs
    $("#other_progs .datepicker").datepicker(options);
}

function setup_interview_formsets()
{
    // see #qualifications etc in interview_edit.html
    $('#qualifications').appendTo('#skillsqual');
    $('#learning').appendTo('#skillsqual');
    $('#plan_train').appendTo('#skillsqual');
    $('#other_agencies').appendTo('#agencies');
    $('#other_progs').appendTo('#agencies');
    // attach formset handler
    setup_inline_formsets();
}

var INLINE_QUALS_SETUP = false;
var INLINE_AGENCIES_SETUP = false;
function setup_inline_formsets()
{
    $('a[href="#skillsqual"]').parent().click(function(){
        if (!INLINE_QUALS_SETUP)
        {
             setTimeout(function(){
                $('#qualifications tbody tr').formset({prefix: 'quals'});
                $('#learning tbody tr').formset({prefix: 'learn'});
                $('#plan_train tbody tr').formset({prefix: 'plan_train'});
            }, 10);
            INLINE_QUALS_SETUP = true;
        }
    });
    $('a[href="#agencies"]').parent().click(function(){
        if (!INLINE_AGENCIES_SETUP)
        {
             setTimeout(function(){
                $('#other_agencies tbody tr').formset({prefix: 'other_agencies'});
                $('#other_progs tbody tr').formset({prefix: 'other_progs'});
            }, 10);
            INLINE_AGENCIES_SETUP = true;
        }
    });
}