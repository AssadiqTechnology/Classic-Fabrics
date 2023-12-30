
    $(document).ready(function() {
        $('.login__input').each(function() {
            $(this).data('default', $(this).val());
        });

        $('.login__input').focus(function() {
            if ($(this).val() === $(this).data('default')) {
                $(this).val('');
            }
        }).blur(function() {
            if ($(this).val() === '') {
                $(this).val($(this).data('default'));
            }
        });
    });
