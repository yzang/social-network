/**
 * Created by Yiming on 2/11/2016.
 */

$('#post-form textarea').on('focus', function () {
    $(this).removeClass('input-error');
});

$('#post-form').on('submit', function (e) {
    $(this).find('textarea').each(function () {
        if ($(this).val() == "" || $(this).val().length>160) {
            e.preventDefault();
            $(this).addClass('input-error');
            console.log("error")
        }
        else {
            $(this).removeClass('input-error');
        }
    });

});