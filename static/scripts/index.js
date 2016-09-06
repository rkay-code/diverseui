$(document).ready(function() {
  var PER_PAGE = 50;
  var IMAGES = window.Data || [];

  var size = 90;
  var gender = 'both';
  var count = PER_PAGE;

  var showImages = function() {
    var images = _.filter(IMAGES, function(image) {
      return gender === 'both' || image.gender === gender;
    }).slice(0, count);

    var imageNodes = _.map(images, function(i) {
      return '<img width="' + size + '" height="' + size + '" src="' + i.url + '" />';
    });

    $('#images').html(imageNodes.join(''));
  };

  $('#load-more').on('click', function() {
    count += PER_PAGE;

    if (count >= IMAGES.length) {
      $('#load-more').remove();
    }

    showImages();
  });

  $('input[type=radio][name="gender"]').change(function() {
    gender = this.value;

    showImages();
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

      showImages();
    }
  });

  showImages(size, gender);
});
