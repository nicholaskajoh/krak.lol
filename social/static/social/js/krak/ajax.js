// ajax requests js

(function($) {

  // convert integer to string with commas e.g 54209 to 54,209
  var itswc = function(i) { return i.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); };

  // LIKE
  $('body').on('click', '.like-button', function() {
    // vars
    var likeButton = $(this);
    likeButton.css("pointerEvents", "none");
    var action = likeButton.data('action'); // like or unlike
    var itemId = likeButton.data('itemId');
    var itemType = likeButton.data('itemType');
    var likesCountElementId = '#'+itemType+'LikesCount'+itemId;
    var likesCount = parseInt($(likesCountElementId).html().replace(/,/g, ''), 10);

    function doLikeUnlike() {
      // toggle like and unlike
      if (action == 'like') {
        likeButton.html('<i class="fa fa-heart liked"></i> Liked ');
        $(likesCountElementId).html(itswc(++likesCount));
        likeButton.data('action', 'unlike');
      } else if (action == 'unlike') {
        likeButton.html('<i class="fa fa-heart like"></i> Like ');
        $(likesCountElementId).html(itswc(--likesCount));
        likeButton.data('action', 'like');
      }
      action = likeButton.data('action');
    }
    doLikeUnlike();

    $.ajax({
      type: "post",
      url: "/like/",
      data: {
        'itemId': itemId,
        'itemType': itemType,
        'csrfmiddlewaretoken': window.CSRF_TOKEN
      },
      success: function (data) {
        // user must be logged in to like
        if (!data.auth) {
          // user not logged
          bootbox.confirm({
            title: "Oops!",
            message: "You must be signed in to like stuff on Krak.lol. Sign In or Sign Up if you don't have an account.", 
            callback: function(do_action){
              if(do_action) {
                window.location = "/auth/?pif=sign_in&next=" + window.PAGE_PATH;
              }
            }
          });
          doLikeUnlike();
        }
        likeButton.css("pointerEvents", "auto");
      },
      error: function(xhr, status, error) {
        if(xhr.status == 0) {
          $.notify({message: "Oh crap... You're offline!"}, {type: 'danger'});
        } else {
          $.notify({message: "Oops! An error occured: "+error+"."}, {type: 'danger'});
        }
        doLikeUnlike();
        likeButton.css("pointerEvents", "auto");
      }
    });
  });

  // FOLLOW USER
  $('body').on('click', '.follow-button', function() {
    var followButton = $(this);
    // make like button unclickable (prevents repeated clicks in a high lateny situation)
    followButton.prop("disabled", true);
    var followedUserId = followButton.data('krakUserId');
    var action = followButton.data('action');

    $.ajax({
      type: 'post',
      url: '/follow/',
      data: {
        'action': action,
        'followedUserId': followedUserId,
        'csrfmiddlewaretoken': window.CSRF_TOKEN
      },
      success: function (data) {
        if (data.auth) {
          if (action == 'follow') {
            followButton.html('Unfollow');
            followButton.data('action', 'unfollow');
            followButton.removeClass('btn-primary');
            followButton.addClass('btn-success');
          } else if(action == 'unfollow') {
            followButton.html('Follow');
            followButton.data('action', 'follow');
            followButton.removeClass('btn-success');
            followButton.addClass('btn-primary');
          }
        } else {
          // user not logged
          bootbox.confirm({
            title: "Err...",
            message: "You must be Signed In to follow someone on Krak.lol. Sign In or Sign Up if you don't have an account.", 
            callback: function(do_action) {
              if(do_action) {
                window.location = "/auth/?pif=sign_in&next=" + window.PAGE_PATH;
              }
            }
          });
        }
        // make like button clickable
        followButton.prop("disabled", false);
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
        // make like button clickable
        followButton.prop("disabled", false);
      }
    });
  });

  // DELETE
  $('body').on('click', '.delete-button', function() {
    var deleteButton = $(this);
    var itemId = deleteButton.data('itemId');
    var itemType = deleteButton.data('itemType');
    var redirectUrl = deleteButton.data('redirectUrl');

    bootbox.confirm({
      title: "Delete",
      message: "Are you sure you want to delete this "+itemType+"?", 
      callback: function(do_action) {
        if (do_action) {
          $.ajax({
            type: 'post',
            url: '/delete/',
            data: {
              'itemId': itemId,
              'itemType': itemType,
              'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function(data) {
              if (!data.error) {
                window.location = redirectUrl;
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
            }
          });
        }
      }
    });
  });

  // COMMENT
  $('body').on('submit', '.comment-form', function() {
    var form = this;
    var jqForm = $(this);
    var postId = jqForm.data('postId');
    var page = jqForm.data('page'); // post page or other
    var commentsCount = parseInt(jqForm.data('commentsCount'));
    var formData = new FormData(this);
    formData.append('post_id', postId);
    formData.append('csrfmiddlewaretoken', window.CSRF_TOKEN);
    var submitCommentBtn = $('#submitCommentBtn'+postId);
    var submitCommentSpinner = $('#submitCommentSpinner'+postId); // spinner is on submit button
    var commentModal = $('#addComment'+postId);

    // disable submit button temporarily
    submitCommentBtn.prop("disabled", true);
    submitCommentSpinner.show();

    // hide any error messages
    $('#contentErrors'+postId).hide();

    $.ajax({
      type: 'post',
      url: '/comment/',
      data: formData,
      success: function(data) {
        if(data.auth) { // if user is authenticated
          if(data.errors) {
            // content input errors
            if(data.errors.content) {
              var errors_html = "";
              data.errors.content.forEach(function(error) {
                errors_html += "<p>"+error+"</p>";
              });
              $('#contentErrors'+postId).html(errors_html);
              $('#contentErrors'+postId).show();
            }
          } else {
            commentModal.modal('hide');
            commentsCount++;
            jqForm.data('commentsCount', commentsCount);
            if(page == "post") { // comment was submitted from post page
              // add comment to the top of the list
              $('#comments').prepend(data.comment_html);
              // update comments count
              $('#commentsCount').html("Comments ("+itswc(commentsCount)+")");
              // if number of comments up to 10,
              // remove the last comment on the list
              if($('#comments li').length >= 10) {
                $('#comments li').last().remove();
              }
            } else if(page == "other") {
              $('#postCommentDivider'+postId).show();
              // add/replace comment in latest comment list
              $('#commentLatest'+postId).html(data.comment_html);
              // update comments count
              $('#commentsCount'+postId).html(itswc(commentsCount));
            }
            // reset form
            form.reset();
            // show notification
            $.notify({
              // options
              message: 'You just posted a comment!'
            },{
              // settings
              type: 'success'
            });
          }
        } else {
          // user not logged
          bootbox.confirm({
            title: "Argh!!!",
            message: "You must be Signed In to comment on a post. Sign In or Sign Up if you don't have an account.", 
            callback: function(do_action){
              if (do_action) {
                window.location = "/?action=sign_in&next=" + window.PAGE_PATH;
              }
            }
          });
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
        // enable submit button
        submitCommentBtn.prop("disabled", false);
        submitCommentSpinner.hide();
      },
      cache: false,
      contentType: false,
      processData: false
    });

    return false;
  });

  // CLEAR IMAGE
  $('#clearImage').on('click', function() {
    var link = $(this);
    var itemId = link.data('itemId');
    var itemType = link.data('itemType');

    bootbox.confirm({
      title: "Clear Image",
      message: "Are you sure you want to remove this image?",
      callback: function(do_action) {
        if(do_action) {
          $.ajax({
            type: 'post',
            url: '/clear-image/',
            data: {
              'itemId': itemId,
              'itemType': itemType,
              'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            success: function(data) {
              window.location.reload(true);
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
            }
          });
        }
      }
    });
  });

}(jQuery));