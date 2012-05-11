(($) ->
  $ ->
    return unless $("body").hasClass("change-form")
    
    $(window).bind('beforeunload', ->
      href = $("#content-main ul.object-tools li a.viewsitelink").attr(
        "href").split("/")
      [_, object_id, content_type_id] = [href.pop(), href.pop(), href.pop()]
      $.ajax
        url: "/admin_locking/unlock/#{content_type_id}/#{object_id}"
        async: false
      null
    )
    
    $("div.admin_locking_page_load_time").hide()
    $("#admin_locking_alter_background").parents("ul.errorlist").removeClass(
      "errorlist").addClass "errornote"
    null
) django.jQuery