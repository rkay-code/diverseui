$(document).ready(function() {
  var IMAGES = window.Data || [];

  var size = 90;
  var gender = 'both';

  var showImages = function(size, gender) {
    var images = _.filter(IMAGES, function(image) {
      return gender === 'both' || image.gender === gender;
    }).slice(0, 50);

    var imageNodes = _.map(images, function(i) {
      return '<img width="' + size + '" height="' + size + '" src="' + i.url + '" />';
    });

    $('#images').html(imageNodes.join(''));
  };

  $('input[type=radio][name="gender"]').change(function() {
    gender = this.value;

    showImages(size, gender);
  });

  $('#size-slider').slider({
    range: 'min',
    value: size,
    min: 32,
    max: 180,
    step: 1,
    slide: function(event, ui) {
      $('#slider-label').html(ui.value + 'px');
      size = ui.value;
      showImages(size, gender);
    }
  });

  showImages(size, gender);
});
