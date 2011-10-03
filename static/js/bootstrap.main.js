(function(window, document, $) {

    // Set up a namespace.
    var ns = {};


    // Search bar functionality.
    var search = $('.magnifying-glass').find('a');
    search.click(function(e) {
        var form = $('#search-bar');
        e.preventDefault();
        form.trigger('submit');
    });


    // Prevent bubbling on dropdown menu.
    var menu = $('.menu-dropdown').find('*');
    menu.click(function(e) {
        e.stopPropagation();
    });


    // Set up home page slides.
    var container = $('.slide_container');

    container.hover(function(e) {
        ns.hover = true;
    }, function(e) {
        ns.hover = false;
    });

    ns.intervalTime = 2000;
    ns.scroll = function() {
        var slider = $('.slider'),
            scrollTop = slider.scrollTop(),
            scrollAmount = 250,
            children = slider.children().length - 1,
            animation;

        if (!ns.hover) {
            if (scrollTop == scrollAmount * children) {
                animation = {scrollTop: 0};
            } else {
                animation = {scrollTop: '+=' + scrollAmount};
            }
            slider.animate(animation);
        }
    }

    // Set up a scroll interval on browsers with hover events.
    // ns.interval = setInterval(ns.scroll, ns.intervalTime);


    var controls = $('.controls');

    controls.bind('hover click', function(e) {
        var parent = $(this).parent(),
            repeatDiv = parent.parent(),
            parentDiv = repeatDiv.parent(),
            slider = $('.slider'),
            scrollAmount = 250,
            index = parent.index(),
            percent = index * 50 + '%';

        e.preventDefault();

        slider.animate({
            scrollTop: scrollAmount * index
        }, 300);

        repeatDiv.animate({
            'background-position': '62% ' + percent
        });

        parentDiv.animate({
            'background-position': '9% ' + percent
        });

    });


    $(window).scroll(function(e) {
        var self = $(this),
            filters = $('.filters'),
            scrollTop = self.scrollTop();

        if (scrollTop > 260) {
            filters.addClass('filters-scrolling');
        } else {
            filters.removeClass('filters-scrolling');
        }
    });



    // Connect namespace with window object.
    window.ns = ns;

})(window, document, jQuery);
