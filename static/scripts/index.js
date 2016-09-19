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
      return ([
        '<img ',
          'crossOrigin="Anonymous" ',
          'class="image" ',
          'width="', size,
          '" height="', size,
          '" src="', i.url, '"',
        ' />'
      ].join(''));
    });

    $('#images').html(imageNodes.join(''));

    if (count >= filtered.length) {
      count = filtered.length;
      $('#load-more-container').html('');
    } else if ($('#load-more-container').html().trim().length === 0) {
      $('#load-more-container').html('<button type="button" id="load-more" class="button">Load More</button>');
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

  var canvas = document.createElement('canvas');
  var context = canvas.getContext('2d');

  var getFolderName = function() {
    var now = new Date();
    var month = ('0' + (now.getMonth() + 1)).slice(-2);
    var date = ('0' + now.getDate()).slice(-2);
    return ['diverseui', month, date].join('-');
  };

  var downloadImages = function(images) {
    var zip = new JSZip();
    var i;
    var imageData;
    var folder = getFolderName();

    canvas.width = size;
    canvas.height = size;

    for (i = 0; i < images.length; i++) {
      context.drawImage(images[i], 0, 0, size, size);
      imageData = canvas.toDataURL().replace(/^data:image\/(png|jpg);base64,/, '');
      zip.file(folder + '/image-' + (i + 1) + '.png', imageData, {base64: true});
    }

    zip.generateAsync({type: 'blob'}).then(function(blob) {
      saveAs(blob, folder + '.zip');
    }, function(err) {
      console.log(err);
    });
  }

  $('.image').on('click', function() {
    $(this).toggleClass('selected-image');
  });

  $('#download-all').on('click', function() {
    var images = document.getElementsByClassName('image');
    downloadImages(images);
  });

  $('#download-selected').on('click', function() {
    var images = document.getElementsByClassName('selected-image');
    downloadImages(images);
  });
});
