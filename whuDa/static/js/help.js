$(document).ready(function () {
    $(".help-hide").hide();
    $(".help-click").hover(function(){
        $(this).children(".help-hide").toggle(500);
    },function(){
        $(this).children(".help-hide").toggle(500);
    });
});