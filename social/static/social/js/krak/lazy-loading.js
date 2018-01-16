// lazy loading js

(function($) {

	// LOAD USER FEEDS (HOME PAGE)
	$('#loadFeeds').on('click', function() {
	    var link = $(this);
	    var page = link.data('page');
	    link.hide();
	    $('#feedSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-feeds/',
	        data: {
	            'page': page,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
	            // add posts to feed
				$('#feed').append(data.list_html);
				// lazy load images from new content
				var blazy = new Blazy();

	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#feedSpinner').hide();
	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load feeds.",
				});
	            link.show();
	            $('#feedSpinner').hide();
	        }
	    });
	});
	
	// LOAD USER LISTS
	$('.load-user-lists').on('click', function() {
	    var link = $(this);
	    var userList = link.data('userList');
	    var page = link.data('page');
	    var userId = link.data('userId');
	    link.hide();
	    $('#'+userList+'Spinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-user-lists/',
	        data: {
	            'userList': userList,
	            'page': page,
	            'userId': userId,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
	            $('#'+userList).append(data.list_html);
	            // lazy load images from new content
				var blazy = new Blazy();
	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#'+userList+'Spinner').hide();

	        },
	        error: function(xhr, status, error) {
                $.notify({
                    // options
                    message: "Oops! An error occured: Couldn't load "+userList+"."
                },{
                    // settings
                    type: 'danger'
                });
	            link.show();
	            $('#'+userList+'Spinner').hide();
	        }
	    });
	});

	// LOAD POPULAR POSTS
	$('#loadPopular').on('click', function() {
	    var link = $(this);
	    var page = link.data('page');
	    link.hide();
	    $('#popularSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-popular/',
	        data: {
	            'page': page,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
				$('#popular').append(data.list_html);
				// lazy load images from new content
				var blazy = new Blazy();

	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#popularSpinner').hide();
	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load posts.",
				});
	            link.show();
	            $('#popularSpinner').hide();
	        }
	    });
	});

	// LOAD POPULAR USERS
	$('#loadUsers').on('click', function() {
	    var link = $(this);
	    var page = link.data('page');
	    link.hide();
	    $('#usersSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-users/',
	        data: {
	            'page': page,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
				$('#users').append(data.list_html);
				// lazy load images from new content
				var blazy = new Blazy();

	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#usersSpinner').hide();
	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load userss.",
				});
	            link.show();
	            $('#usersSpinner').hide();
	        }
	    });
	});

	// LOAD COMMENTS
	$('#loadComments').on('click', function() {
	    var link = $(this);
	    var page = link.data('page');
	    var postId = link.data('postId');
	    link.hide();
	    $('#loadCommentsSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-comments/',
	        data: {
	            'page': page,
	            'postId': postId,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
	            $('#comments').append(data.comments_html);
	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#loadCommentsSpinner').hide();

	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load comments.",
				});
	            link.show();
	            $('#loadCommentsSpinner').hide();
	        }
	    });
	});

	// LOAD SEARCH RESULTS
	$('#loadSearchResults').on('click', function() {
	    var link = $(this);
	    var query = link.data('query');
	    var page = link.data('page');
	    var postId = link.data('postId');
	    link.hide();
	    $('#loadSearchResultsSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-search-results/',
	        data: {
	        	'q': query,
	            'page': page,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
	            $('#searchResults').append(data.results_html);
	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#loadSearchResultsSpinner').hide();

	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load search results.",
				});
	            link.show();
	            $('#loadSearchResultsSpinner').hide();
	        }
	    });
	});

	// LOAD NOTIFICATIONS
	$('body').on('click', '#loadNotifications', function() {
	    var link = $(this);
	    var page = link.data('page');
	    var postId = link.data('postId');
	    link.hide();
	    $('#loadNotificationsSpinner').show();

	    $.ajax({
	        type: 'post',
	        url: '/load-notifications/',
	        data: {
	            'page': page,
	            'csrfmiddlewaretoken': window.CSRF_TOKEN
	        },
	        success: function(data) {
	            $('#notifications').append(data.notifs_html);
	            if (data.has_next) {
	                link.show();
	                link.data('page', page+1);
	            }
	            $('#loadNotificationsSpinner').hide();

	        },
	        error: function(xhr, status, error) {
	            bootbox.alert({
					title: "Error",
					message: "Oops! An error occured: Couldn't load notifications.",
				});
	            link.show();
	            $('#loadNotificationsSpinner').hide();
	        }
	    });
	});

}(jQuery));