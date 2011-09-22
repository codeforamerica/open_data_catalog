(function(window, $) {
    var search = $('.magnifying-glass').find('a');
    search.click(function(e) {
        var form = $('#search-bar');
        e.preventDefault();
        form.trigger('submit');
    });
})(window, jQuery);
