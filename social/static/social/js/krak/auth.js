// authentication js

(function($) {

    // SIGN IN
    $('#signInForm').on('submit', function() {
        var formData = new FormData(this);
        var signInButton = $('#signInButton');
        var signInSpinner = $('#signInSpinner');

        // disable sign in button temporarily
        signInButton.prop("disabled", true);
        signInSpinner.show();

        $.ajax({
            type: 'post',
            url: '/auth/',
            data: formData,
            success: function(data) {
                if(data.errors) {
                    // display error
                    var errors_html = "";
                    data.errors.forEach(function(error) {
                        errors_html += "<p>"+error+"</p>";
                    });
                    $('#signInError').html(errors_html);
                    $('#signInError').show();
                } else {
                    // redirect to next page
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
                // enable sign in button
                signInButton.prop("disabled", false);
                signInSpinner.hide();
            },
            cache: false,
            contentType: false,
            processData: false
        });

        return false;
    });

    // SIGN UP
    $('#signUpForm').on('submit', function() {
        var formData = new FormData(this);
        var signUpButton = $('#signUpButton');
        var signUpSpinner = $('#signUpSpinner');

        // disable sign in button temporarily
        signUpButton.prop("disabled", true);
        signUpSpinner.show();

        // hide any error messages
        $('#sfOtherErrors').hide();
        $('#sfUsernameErrors').hide();
        $('#sfEmailErrors').hide();

        $.ajax({
            type: 'post',
            url: '/auth/',
            data: formData,
            success: function(data) {
                if(data.errors) {
                    // other form errors
                    if(data.errors.__all__) {
                        var errors_html = "";
                        data.errors.__all__.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#sfOtherErrors').html(errors_html);
                        $('#sfOtherErrors').show();
                    }

                    // username input errors
                    if(data.errors.username) {
                        var errors_html = "";
                        data.errors.username.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#sfUsernameErrors').html(errors_html);
                        $('#sfUsernameErrors').show();
                    }

                    // email input errors
                    if(data.errors.email) {
                        var errors_html = "";
                        data.errors.email.forEach(function(error) {
                            errors_html += "<p>"+error+"</p>";
                        });
                        $('#sfEmailErrors').html(errors_html);
                        $('#sfEmailErrors').show();
                    }
                } else {
                    // redirect to next page
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
                // enable sign in button
                signUpButton.prop("disabled", false);
                signUpSpinner.hide();
            },
            cache: false,
            contentType: false,
            processData: false
        });
        
        return false;
    });

}(jQuery));