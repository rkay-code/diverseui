$(document).ready(function() {
  var PER_PAGE = 50;
  var IMAGES = window.Data || [];

  var size = 78;
  var gender = 'neutral';
  var count = PER_PAGE;

  var filteredImages = function() {
    return _.filter(IMAGES, function(image) {
      return gender === 'neutral' || image.gender === gender;
    });
  };

  var resizeImages = function() {
    var images = document.getElementsByClassName('image');
    var i;
    var image;

    for (i = 0; i < images.length; i++) {
      image = images[i];
      image.height = size;
      image.width = size;
    }
  };

  var showImages = function(options) {
    var from = options.from === undefined ? count : options.from;
    var to = options.to === undefined ? (from + PER_PAGE) : options.to;
    var append = !!options.append;

    var filtered = filteredImages();
    var images = filtered.slice(from, to);

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

    if (append) {
      $('#images').append(imageNodes.join(''));
    } else {
      $('#images').html(imageNodes.join(''));

      $('#download-selected').addClass('disabled');
    }

    count = to;

    if (count >= filtered.length) {
      count = filtered.length;
      $('#load-more-container').html('');
    } else if ($('#load-more-container').html().trim().length === 0) {
      $('#load-more-container').html('<button type="button" id="load-more" class="button">Load More</button>');
    }
  };

  $('#load-more-container').on('click', '#load-more', function() {
    showImages({append: true});
  });

  $('select').change(function() {
    gender = this.value;

    showImages({from: 0, to: count, append: false});
  });

  var $sliderLabel = $('<span class="slider-label">78px</span>');

  $('#size-slider').slider({
    range: 'min',
    value: size,
    min: 32,
    max: 180,
    step: 1,
    create: function() {
      $('.ui-slider-handle').append($sliderLabel);
    },
    slide: function(event, ui) {
      $sliderLabel.html(ui.value + 'px');
      size = ui.value;
      resizeImages();
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

  var downloadImages = function(images, button) {
    if (!images.length) {
      return;
    }

    var zip = new JSZip();
    var i;
    var imageData;
    var folder = getFolderName();
    var initialText = button.innerHTML;

    if (window.ga) {
      ga('send', {
        hitType: 'event',
        eventCategory: 'Button',
        eventAction: 'Download',
        eventLabel: initialText,
        eventValue: images.length
      });
    }

    // Show LOADING if downloading more than 10 images
    if (images.length > 10) {
      button.innerHTML = 'LOADING...';
    }

    canvas.width = size;
    canvas.height = size;

    for (i = 0; i < images.length; i++) {
      context.drawImage(images[i], 0, 0, size, size);
      imageData = canvas.toDataURL().replace(/^data:image\/(png|jpg);base64,/, '');
      zip.file(folder + '/image-' + (i + 1) + '.png', imageData, {base64: true});
    }

    zip.generateAsync({type: 'blob'}).then(function(blob) {
      button.innerHTML = initialText;
      saveAs(blob, folder + '.zip');
    }, function(err) {
      button.innerHTML = initialText;
      console.log(err);
    });
  }

  $('#images').on('click', '.image', function() {
    $(this).toggleClass('selected-image');

    $('#download-selected').toggleClass('disabled', !$('.selected-image').length);
  });

  $('#download-all').on('click', function() {
    var button = this;
    var images = document.getElementsByClassName('image');
    downloadImages(images, button);
  });

  $('#download-selected').on('click', function() {
    var button = this;
    var images = document.getElementsByClassName('selected-image');
    downloadImages(images, button);
  });
});
