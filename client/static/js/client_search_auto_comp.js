$(function() {
    setup_quick_client_auto_comp();
});

function setup_quick_client_auto_comp()
{
    $("#quick_client").autocomplete({
        source: "/auto/quick_client_search/",
        select: function (event, ui) { //item selected
            action_client_selected(event, ui)
        },
        minLength: 1,
    });
}

function action_client_selected(event, ui)
{
    var client_obj = ui.item;
    window.location.href = '/client/' + client_obj.id + '/edit';
}