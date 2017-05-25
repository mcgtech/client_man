$(function(){
    setup_table_filters();
});

function setup_table_filters()
{
     remove_please_select();
     setup_filter_datepickers();
}

function remove_please_select()
{
     $("form select option:contains('Please select')").remove();
}

function setup_filter_datepickers()
{
    var options = get_basic_date_picker_options();
    $(".datepicker").datepicker(options);
}