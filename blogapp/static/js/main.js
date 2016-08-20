// open and close accordions
function control_accordion(id) {
    var x = document.getElementById(id);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
}
<<<<<<< HEAD
=======

$(document).ready(function() {
  $('#nav-container').load('/static/main-menu.html', function(){
    var idMenu = $('#nav-container').attr('class');
    $('#'+idMenu).addClass('w3-text-teal');
  });
});
>>>>>>> 2f37020f89ca8ca91372417bca016b76c96ec971
