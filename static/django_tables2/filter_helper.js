$(function(){
    setup_table_filters();
});

function setup_table_filters()
{
     remove_please_select();
}

function remove_please_select()
{
     $("form select option:contains('Please select')").remove();
}