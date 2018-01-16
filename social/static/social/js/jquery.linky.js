/**
 * jquery.linky.js v0.1.8
 * https://github.com/AnSavvides/jquery.linky
 * The MIT License (MIT)
 *
 * Copyright (c) 2013 - 2015 Andreas Savvides
 * 
 * Customized to allow any link-to base url
 * So you're not limited to Twitter, Instagram or GitHub
 * Plus other hacks
 */
(function($) {

    "use strict";

    $.fn.linky = function(options) {
        return this.each(function() {
            var $el = $(this),
                linkifiedContent = _linkify($el, options);

            $el.html(linkifiedContent);
        });
    };

    function _linkify($el, options) {
        var defaultOptions = {
            mentions: false,
            hashtags: false,
            urls: true,
            baseUrl: "/",
            hashtagsSearchPath: "tagged/"
        };
        var extendedOptions = $.extend(defaultOptions, options);
        var elContent = $el.html();
        // Regular expression courtesy of Matthew O'Riordan, see: http://goo.gl/3syEKK
        var urlRegEx = /((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-]*)?\??(?:[\-\+=&;%@\.\w]*)#?(?:[\.\!\/\\\w]*))?)/g;
        var matches;

            // Linkifying URLs
            if (extendedOptions.urls) {
                matches = elContent.match(urlRegEx);
                if (matches) {
                    elContent = _linkifyUrls(matches, $el);
                }
            }

            // Linkifying mentions
            if (extendedOptions.mentions) {
                elContent = _linkifyMentions(elContent, extendedOptions.baseUrl);
            }

            // Linkifying hashtags
            if (extendedOptions.hashtags) {
                elContent = _linkifyHashtags(elContent, extendedOptions.baseUrl, extendedOptions.hashtagsSearchPath);
            }

        return elContent;
    }

    // For any URLs present, unless they are already identified within
    // an `a` element, linkify them.
    function _linkifyUrls(matches, $el) {
        var elContent = $el.html();

        $.each(matches, function() {
            // Only linkify URLs that are not already identified as
            // `a` elements with an `href`.
            if ($el.find("a[href='" + this + "']").length === 0) {
                var url = this;
                if (this.indexOf('http://') == -1 && this.indexOf('https://') == -1) {
                    url = '//' + this;
                    matches[matches.indexOf(this)] = url;
                }
                elContent = elContent.replace(this, "<a href='" + url + "' target='_blank'>" + this + "</a>");
            }
        });

        return elContent;
    }

    // Find any mentions (e.g. @andrs) and turn them into links that
    // refer to the appropriate profile of a given website.
    function _linkifyMentions(text, baseUrl) {
        return text.replace(/(^|\s|\(|>)@(\w+)/g, "$1<a href='" + baseUrl + "@$2'>@$2</a>");
    }

    // Find any hashtags (e.g. #linkyrocks) and turn them into links that
    // refer to the appropriate tag page of a given website.
    function _linkifyHashtags(text, baseUrl, hashtagsSearchPath) {
        // If there is no search URL for a hashtag, there isn't much we can do
        if (hashtagsSearchPath === null) return text;
        return text.replace(/(^|\s|\(|>)#((\w|[\u00A1-\uFFFF])+)/g, "$1<a href='" + baseUrl + hashtagsSearchPath + "$2'>#$2</a>");
    }

}(jQuery));