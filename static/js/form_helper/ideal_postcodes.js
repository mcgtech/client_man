$(function(){
     setup_postcode_lookup();
});

// https://ideal-postcodes.co.uk/jquery
function setup_postcode_lookup() {
    add_lookup_field_to_dom();
    $('#lookup_field').setupPostcodeLookup({
          api_key: 'ak_i2d5odc4INouNMPRJ3mtcV1igzrnG', // TODO: put into variable and create newone for shirlie
          output_fields: {
            line_1: '#id_address-line_1',
            line_2: '#id_address-line_2',
//            line_3: '#id_address-line_3',
            post_town: '#id_address-line_3',
            postcode: '#id_address-post_code'
          },
          onSearchCompleted: function (data) {
            $('#idpc_dropdown').addClass('select form-control');
          },
            button_class: 'btn btn-primary',
            input_class: 'form-control'
        });
}

function add_lookup_field_to_dom()
{
    $('.row.postcode').append('<label class="control-label pc-lookup">Post code lookup</label><div class="col-sm-6 pc-lookup"><div id="lookup_field"></div></div>');
}