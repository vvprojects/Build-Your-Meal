$(document).on('submit', '#adress_input_form', function(e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: 'parse_adress/',
        data: {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function () { window.alert("Парсер закончил работу.");}
    });

    return false;
});
