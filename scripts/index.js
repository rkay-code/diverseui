var IMAGES = [
  {gender: 'male', src: 'http://static5.depositphotos.com/1010683/424/i/950/depositphotos_4241802-Asian-man-with-glass.jpg'},
  {gender: 'male', src: 'http://www.abcsofattraction.com/blog/wp-content/uploads/2012/10/poker-face-3.jpg'},
  {gender: 'male', src: 'http://www.mens-hairstylists.com/wp-content/uploads/2015/10/Hairstyle-for-Asian-men.jpg'},
  {gender: 'female', src: 'http://www.asianonlinesingles.com/wp-content/uploads/2012/04/Dating-Asian-Woman-and-be-Successful.jpg'},
  {gender: 'female', src: 'http://blindgossip.com/wp-content/uploads/2011/08/asian-woman-1.jpg'},
];

$(document).ready(function() {
  var size = 90;
  var gender = 'both';

  var showImages = function(size, gender) {
    var images = _.filter(IMAGES, function(image) {
      return gender === 'both' || image.gender === gender;
    });

    var imageNodes = _.map(images, function(i) {
      return '<img width="' + size + '" height="' + size + '" src="' + i.src + '" />';
    });

    $('#images').html(imageNodes.join(''));
  };

  $('input[type=radio][name="gender"]').change(function() {
    gender = this.value;

    showImages(size, gender);
  });

  $('#size-slider').slider({
    value: 90,
    min: 32,
    max: 180,
    change: function(event, ui) {
      size = ui.value;
      showImages(size, gender);
    },
    slide: function(event, ui) {
      $('#slider-label').html(ui.value);
      size = ui.value;
      showImages(size, gender);
    }
  });

  $("#slider-label").html(size);

  showImages(size, gender);

});
