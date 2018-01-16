// post forms js

(function($) {

	// CREATE OR EDIT A POST
	$('.post-form').on('submit', function() {
		var formData = new FormData(this);
		var form = $(this);
		var formType = form.data('formType'); // new or edit post
		var postButton = $('#'+formType+'Button');
        var postSpinner = $('#'+formType+'Spinner');

        // disable post button temporarily
        postButton.prop("disabled", true);
        postSpinner.show();

		// hide any error messages
        $('#'+formType+'OtherErrors').hide();
        $('#'+formType+'TitleErrors').hide();
        $('#'+formType+'ContentErrors').hide();
        $('#'+formType+'FeaturedImageErrors').hide();

		$.ajax({
            type: 'post',
            url: '/post/',
            data: formData,
            success: function(data) {
            	if(data.errors) {
            		// other form errors
                    if(data.errors.__all__) {
                        var errors_html = "";
                        data.errors.__all__.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#'+formType+'OtherErrors').html(errors_html);
                        $('#'+formType+'OtherErrors').show();
                    }

                    // title input errors
                    if(data.errors.title) {
                        var errors_html = "";
                        data.errors.title.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#'+formType+'TitleErrors').html(errors_html);
                        $('#'+formType+'TitleErrors').show();
                    }

                    // content input errors
                    if(data.errors.content) {
                        var errors_html = "";
                        data.errors.content.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#'+formType+'ContentErrors').html(errors_html);
                        $('#'+formType+'ContentErrors').show();
                    }

                    // featured_image input errors
                    if(data.errors.featured_image) {
                        var errors_html = "";
                        data.errors.featured_image.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#'+formType+'FeaturedImageErrors').html(errors_html);
                        $('#'+formType+'FeaturedImageErrors').show();
                    }
            	} else {
            		// redirect to new or edited post
            		window.location = data.next;
            	}
            },
            error: function(xhr, status, error) {
                if(xhr.status == 0) {
                    bootbox.alert({
                        title: "Error",
                        message: "Oh crap... You're offline!"
                    });
                } else {
                    bootbox.alert({
                        title: "Error",
                        message: "Oops! An error occured: "+error+"."
                    });
                }
            },
            complete: function() {
            	// enable post button
                postButton.prop("disabled", false);
                postSpinner.hide();
            },
            cache: false,
            contentType: false,
            processData: false
        });

		return false;
	});

}(jQuery));