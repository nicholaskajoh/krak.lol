// GENERAL

(function($) {

  // site's base url
  var baseUrl = window.location.protocol+"//"+window.location.host+"/";

  // get GET param from url
  window.GET_URL_PARAM = function(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
      sURLVariables = sPageURL.split('&'),
      sParameterName,
      i;

    for (i = 0; i < sURLVariables.length; i++) {
      sParameterName = sURLVariables[i].split('=');

      if (sParameterName[0] === sParam) {
        return sParameterName[1] === undefined ? true : sParameterName[1];
      }
    }
  };

  // OPEN SIGN IN/UP MODALS
  // if get param "action" == "sign_in" or "sign_up"
  if(window.GET_URL_PARAM('action') == "sign_in") {
    $('#signIn').modal('show');
  } else if(window.GET_URL_PARAM('action') == "sign_up") {
    $('#signUp').modal('show');
  }

  // POST CONTENT LINKFY
  $(".linkify").linky({
    mentions: true,
    hashtags: true,
    urls: true,
    baseUrl: baseUrl,
    hashtagsSearchPath: "tagged/"
  });

  // READ MORE
  $('body').on('click', '.read-more', function() {
    var rmBtn = $(this);
    var postExcerpt = rmBtn.data('excerpt');
    var fullPost = rmBtn.data('full');
    $('#'+postExcerpt).hide();
    $('#'+fullPost).show();
  });

  // BLAZY IMAGE LAZY LOADING
  var blazy = new Blazy();

  // NOTIFICATIONS MODAL (LAUNCH)
  $("#notifsModal").on("show.bs.modal", function(e) {
    var notifsModal = $(this);
    var link = $(e.relatedTarget);
    var notifsSpinner = $('#notifsSpinner');
    notifsSpinner.show();
    $(this).find(".modal-body").load(link.attr("href"), function(response, status, xhr) {
      if(status == "error") {
        notifsModal.modal('hide');
        if(xhr.status == 0) {
          bootbox.alert({
            title: "Error",
            message: "Oh crap... You're offline!"
          });
        } else {
          bootbox.alert({
            title: "Error",
            message: "Oops! An error occured: "+xhr.statusText+"."
          });
        }
      } else {
        $('.badge-notify').hide();
        notifsSpinner.hide(); 
      }
    });
  });

}(jQuery));