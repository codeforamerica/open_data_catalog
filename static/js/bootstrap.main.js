(function(window, $) {

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

})(window, jQuery);
