function updateContainer() {
    var w = $(window).innerWidth();
    if (w > 750) {
           $("#bodyblock").css('margin', "20px 20px 20px 220px");
    } else {
           $("#bodyblock").css('margin', "20px");
           }
    };

$(document).ready(function() {

    $( "#about-btn" ).click(function() {
        alert('test');
        return false;
    });

    $("p").hover( function() {
    $(this).css('color', 'red');
    },
    function() {
    $(this).css('color', 'blue');
    });

    updateContainer();
    $(window).resize(function() {
    console.log('updating');
    updateContainer();
    });

});




