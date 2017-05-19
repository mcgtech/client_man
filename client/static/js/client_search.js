$(function(){
    setup_client_search();
});

function setup_client_search()
{
    //https://www.datatables.net/
    $('#client_results').DataTable({
        "order": [[ 0, "asc" ]]
    } );
}
