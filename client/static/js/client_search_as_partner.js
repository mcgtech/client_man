$(function(){
    $('td.contracts a').each(function(){
        var text = $(this).html();
        $(this).replaceWith(text);
    });
});
