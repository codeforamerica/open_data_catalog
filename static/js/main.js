(function(window, $) {

    // Set up a namespace.
    var ns = {
        dom: {},
        event: {},
        cache: {}
    };

    ns.event.searchFocus = function(e) {
        // Event that takes when the search bar becomes focused.
        var self = $(this),
            time = 200,
            animation;

        if (e.type == 'focusin') {
            //animation = { width: '+=25%' };
        } else {
            //animation = { width: '100%' };
        }

        self.animate(animation, time);
    }

    ns.event.ajaxAutocomplete = function(request, callback) {
        // Autocomplete functionality for searching.
        var term = request.term,
            cache = ns.cache;

        if (term in cache) {
            // Serve the cached response.
            callback(cache[term]);
            return;
        }

        $.ajax({
            url: '/autocomplete',
            dataType: 'json',
            data: {
                q: term
            },
            success: function(data) {
                var cache = ns.cache,
                    response;

                response = $.map(data.tags, function(item) {
                    return {
                        label: item,
                        value: item
                    }
                });

                cache[term] = response;
                callback(response);
            }
        });
    }

    ns.dom.search = function() {
        // Bind the searchFocus function and add autocomplete.
        var search = $('.search_bar');
        search.autocomplete({
            source: ns.event.ajaxAutocomplete,
            select: function(e) {
                var form = $('form');
                form.submit();
            }
        });
        return this;
    }

    ns.event.navigationHover = function(e) {
        // Only navigation links with subnavigation menus will
        // be called with this function.
        var self = $(this),
            subnav = self.find('.subnav'),
            link = subnav.siblings('.links');
        if (subnav.is(':visible')) {
            subnav.hide();
            link.removeClass('navigation_hover');
        } else {
            subnav.show();
            link.addClass('navigation_hover');
        }
    }

    ns.dom.navigation = function() {
        // Navigation links should show subnavigation menus
        // on hover.
        var nav = $('.links').parent(),
            navigationHover = ns.event.navigationHover;
        nav.hover(navigationHover);
        return this;
    }

    ns.event.stopBubbling = function(e) {
        e.stopPropagation();
    }

    ns.event.login = function(e) {
        // Event that fires when the login button is hovered over.
        var self = $(this),
            form = self.siblings('form'),
            gravatar = $('.gravatar'),
            body = $(document.body),
            stopBubbling = ns.event.stopBubbling,
            hideLoginForm = ns.event.hideLoginForm;

        if (gravatar.length > 0) {
            // This should involve logging out.
        } else {
            self.addClass('login_form_open')
                .click(stopBubbling);

            form.show()
                .click(stopBubbling);

            body.click(hideLoginForm)
                .find('nav').hover(hideLoginForm);
        }
    }

    ns.event.hideLoginForm = function(e) {
        var form = $('.login_form'),
            button = form.siblings('a');
        if (form.is(':visible')) {
            form.hide();
            button.removeClass('login_form_open');
        }
    }

    ns.dom.loginButton = function() {
        var button = $('.login_button'),
            login = ns.event.login;
        button.hover(login);
        return this;
    }

    ns.event.supportProject = function(e) {
        var self = $(this),
            form = $('.support_project'),
            csrf = form.children('div').children('input').val(),
            project = form.children('p').eq(0).children('input').val(),
            url = form.attr('action');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'csrfmiddlewaretoken': csrf,
                'project': project
            },
            dataType: 'JSON',
            success: function(data) {
                // Support button should disappear, and the user should be
                // notified he/she is now a supporter.
                console.log(data);
                alert('YAY!');
            },
            error: function(data){
                // The user should be notified he/she needs to log in.
                console.log(data);
                alert('Error!');
            }
        });
    }

    ns.dom.supportButton = function() {
        var button = $('.support_button'),
            supportProject = ns.event.supportProject;
        button.click(supportProject);
        return this;
    }

    ns.dom.communityScroller = function() {
        var carousel = $('#mycarousel');
        if (carousel.length > 0) {
            carousel.jcarousel({
                scroll: 5,
                wrap: 'circular'
            });
        }
        return this;
    }

    ns.dom.init = function() {
        // Initalize function for DOM functionality.
        var dom = ns.dom;
        dom.search()
           .navigation()
           .loginButton()
           .supportButton()
           .communityScroller()
    }

    ns.main = (function() {
        // Anonymous function that acts much like C's ``int main``.
        var dom = ns.dom;
        dom.init();

        // Bind the namespace function to the window.
        window.ns = ns;

        // Just making sure that it executed.
        return true;
    })();


})(window, jQuery);
