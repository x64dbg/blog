function imageClick() {
    $("#largeImage").html("<img src=\"" + $(this).attr("src") + "\" alt=\"" + $(this).attr("alt") + "\">");
    $("#largeImage").fadeIn(800);
    $("#largeImage img").fadeIn(1000);
}

function largeImageClick() {
    $("#largeImage").fadeOut(1000);
    $("#largeImage img").fadeOut(500);
}

$(document).ready(function() {
    $(".post img").click(imageClick);
    $("#largeImage").click(largeImageClick);
});