function populate_print_area(entity_ids, report_id)
{
    var entity_ids = entity_ids.join(',');
    $('#print_area').html('').load('/show_report/' + entity_ids + '/' + report_id +  '/', '', function(response, status, xhr) {
        if (status == 'error')
        {
            var msg = "Sorry but there was a printing error: " + xhr.status + " " + xhr.statusText;
            bootbox.alert(message);
        }
        else
        {
            $('#print_area').printThis();
        }
        });
}