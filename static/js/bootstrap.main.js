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
            slider = $('.slider'),
            scrollAmount = 250,
            index = parent.index() - 1;

        e.preventDefault();

        slider.animate({
            scrollTop: scrollAmount * index
        }, 600);
    });


    // Connect namespace with window object.
    window.ns = ns;

})(window, document, jQuery);
