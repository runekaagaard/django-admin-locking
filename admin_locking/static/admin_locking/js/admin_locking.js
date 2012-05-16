// Generated by CoffeeScript 1.3.1
(function() {

  window.beforeunload_callbacks = window.beforeunload_callbacks || [];

  (function($) {
    return $(function() {
      var callback;
      if (!$("body").hasClass("change-form")) {
        return;
      }
      callback = function() {
        var content_type_id, href, object_id, _, _ref;
        href = $("#content-main ul.object-tools li a.viewsitelink").attr("href").split("/");
        _ref = [href.pop(), href.pop(), href.pop()], _ = _ref[0], object_id = _ref[1], content_type_id = _ref[2];
        $.ajax({
          url: "/admin_locking/unlock/" + content_type_id + "/" + object_id,
          async: false
        });
        return null;
      };
      window.beforeunload_callbacks.push(callback);
      $(window).bind('beforeunload', function() {
        var callback, last, result, _i, _len, _ref;
        _ref = window.beforeunload_callbacks;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          callback = _ref[_i];
          result = callback();
          if (result != null) {
            last = result;
          }
        }
        return last;
      });
      $("div.admin_locking_page_load_time").hide();
      $("#admin_locking_alter_background").parents("ul.errorlist").removeClass("errorlist").addClass("errornote");
      return null;
    });
  })(django.jQuery);

}).call(this);
