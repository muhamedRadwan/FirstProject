var name=2
$(document).ready(function () {
    $(".Add").hide();
    $("#appear").hide();
    $("#r1").click(function () {
        $(".Add").show();
    });
    $("#r2").click(function () {
        $(".Add").hide();
    });
    $('#error').click(function () {
       $('#appear').show();
    });
    $('#disappear').click(function () {
       $('#appear').hide();
    });
    $('#ok').click(function () {
       $('#appear').hide();
    });
});
