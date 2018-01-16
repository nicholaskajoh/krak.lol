// modifications to bootstrap

(function($) {
	// FILE UPLOAD
	$(document).on('click', '.choose-file', function(){
		var file = $(this).parent().parent().parent().find('.file');
		file.trigger('click');
	});

	$(document).on('change', '.file', function(){
		$(this).parent().find('.form-control').val($(this).val().replace(/C:\\fakepath\\/i, ''));
	});


	// SEARCH (FULL SCREEN)
	$('a[href="#search"]').on('click', function(event) {
        event.preventDefault();
        $('#search').addClass('open');
        $('#search > form > input[type="search"]').focus();
    });
    
    $('#search, #search button.close').on('click keyup', function(event) {
        if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
            $(this).removeClass('open');
        }
    });

}(jQuery));