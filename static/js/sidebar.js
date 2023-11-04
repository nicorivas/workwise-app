jQuery("#sidebar").find(".nav-link").hover(
    function() {
        if (jQuery("#sidebar").hasClass("collapsed")) {
            jQuery(this).find(".tooltip").css('opacity','1.0');
        }
    },
    function () {
        if (jQuery("#sidebar").hasClass("collapsed")) {
            jQuery(this).find(".tooltip").css('opacity','0.0');
        }
    }
);

jQuery(".nav-link").on("click",  function() {
    jQuery(".nav-link").removeClass("active");
    jQuery(this).addClass("active");
    jQuery(".nav-link-text").hide();
    jQuery("#sidebar").addClass("collapsed")
    jQuery(".nav-link").find(".text").hide();
});

// If url is not index, then set active item depending on url and collapse menu
if (window.location.pathname != "/") {
    jQuery(".nav-link").removeClass("active");
    jQuery(".nav-link[hx-post='/" + window.location.pathname.split("/")[1] + "/']").addClass("active");
    jQuery(".nav-link-text").hide();
    jQuery("#sidebar").addClass("collapsed")
}