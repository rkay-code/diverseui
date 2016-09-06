$(document).ready(function() {
  var PER_PAGE = 50;
  var IMAGES = window.Data || [];

  var size = 90;
  var gender = 'both';
  var count = PER_PAGE;

  var filteredImages = function() {
    return _.filter(IMAGES, function(image) {
      return gender === 'both' || image.gender === gender;
    });
  };

  var showImages = function() {
    var filtered = filteredImages();
    var images = filtered.slice(0, count);

    var imageNodes = _.map(images, function(i) {
      return '<img width="' + size + '" height="' + size + '" src="' + i.url + '" />';
    });

    $('#images').html(imageNodes.join(''));

    if (count >= filtered.length) {
      count = filtered.length;
      $('#load-more-container').html('');
    } else if ($('#load-more-container').html().trim().length === 0) {
      $('#load-more-container').html('<button type="button" id="load-more">Load More</button>');
    }
  };

  $('#load-more-container').on('click', '#load-more', function() {
    count += PER_PAGE;

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

  showImages();
});
