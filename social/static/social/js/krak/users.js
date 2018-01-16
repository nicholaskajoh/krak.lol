// users js

(function($) {

	// EDIT PROFILE
	$('#editProfileForm').on('submit', function() {
		var formData = new FormData(this);
		var editProfileSubmitBtn = $('#editProfileSubmitBtn');
		var editProfileSpinner = $('#editProfileSpinner');

		// disable save button temporarily
        editProfileSubmitBtn.prop("disabled", true);
        editProfileSpinner.show();

        // hide any error messages
        $('#editProfileOtherErrors').hide();
        $('#editProfileFullNameErrors').hide();
        $('#editProfileBioErrors').hide();
        $('#editProfileLinkErrors').hide();
        $('#editProfileProfilePhotoErrors').hide();

		$.ajax({
            type: 'post',
            url: '/edit-profile/',
            data: formData,
            success: function(data) {
                if(data.errors) {
                	// other form errors
                    if(data.errors.__all__) {
                        var errors_html = "";
                        data.errors.__all__.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#editProfileOtherErrors').html(errors_html);
                        $('#editProfileOtherErrors').show();
                    }

                    // full name input errors
                    if(data.errors.full_name) {
                        var errors_html = "";
                        data.errors.full_name.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#editProfileFullNameErrors').html(errors_html);
                        $('#editProfileFullNameErrors').show();
                    }

                    // bio input errors
                    if(data.errors.bio) {
                        var errors_html = "";
                        data.errors.bio.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#editProfileBioErrors').html(errors_html);
                        $('#editProfileBioErrors').show();
                    }

                    // link input errors
                    if(data.errors.link) {
                        var errors_html = "";
                        data.errors.link.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#editProfileLinkErrors').html(errors_html);
                        $('#editProfileLinkErrors').show();
                    }

                    // profile photo errors
                    if(data.errors.profile_photo) {
                        var errors_html = "";
                        data.errors.profile_photo.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#editProfileProfilePhotoErrors').html(errors_html);
                        $('#editProfileProfilePhotoErrors').show();
                    }
                } else {
                	window.location.reload(true);
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
                // enable save button
                editProfileSubmitBtn.prop("disabled", false);
                editProfileSpinner.hide();
            },
            cache: false,
            contentType: false,
            processData: false
        });

		return false;
	});

}(jQuery));