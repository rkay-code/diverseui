$(document).ready(function() {
  window.Data.forEach(function(image) {
    $('body').append('<img height="50" width="50" src="' + image.url + '" />');
  });
});
