$(function(){
    setup_tags();
    setup_testing_template();
})

function setup_tags()
{
    $('#client_reflections').appendTo('#tags');
}

function setup_testing_template()
{
    $('#test_email_temp').appendTo('#test');
    $('#test_email').click(function(){
        var client_id = $.trim($('#client_id').val());
        var email = $.trim($('#email_to').val());
        var temp_id = $('#id_main-template_identifier').val();
        if (temp_id == "")
        {
            bootbox.alert('Please select a template');
        } else if (!$.isNumeric(client_id))
        {
            bootbox.alert('Please enter a valid client id');
        }
        else if (email.length == 0)
        {
            bootbox.alert('Please enter a valid email address');
        }
        else
        {
            window.location.href = '/email_temp_test/' + temp_id + '/' + client_id + '/' + email + '/';
        }
    });
}