var BOTH = 'BOTH';
var MALE = 'MALE';
var FEMALE = 'FEMALE';

var App = React.createClass({
  propTypes: {
    images: React.PropTypes.array
  },

  getDefaultProps: function() {
    return {
      images: []
    };
  },

  getInitialState: function() {
    return {
      size: 90,
      gender: BOTH
    };
  },

  selectSize: function(newSize) {
    this.setState({
      size: newSize
    });
  },

  selectGender: function(newGender) {
    this.setState({
      gender: newGender
    });
  },

  render: function() {
    var gender = this.state.gender;
    var size = this.state.size;

    var images = _.filter(this.props.images, function(image) {
      return gender === BOTH || image.gender === gender;
    });

    return (
      <div>
        <div>
          <Size size={size} onSelect={this.selectSize} />
          <Gender gender={gender} onSelect={this.selectGender} />
        </div>
        <Images size={size} images={images} />
      </div>
    );
  }
});

var IMAGES = [
  {gender: MALE, src: 'http://static5.depositphotos.com/1010683/424/i/950/depositphotos_4241802-Asian-man-with-glass.jpg'},
  {gender: MALE, src: 'http://www.abcsofattraction.com/blog/wp-content/uploads/2012/10/poker-face-3.jpg'},
  {gender: MALE, src: 'http://www.mens-hairstylists.com/wp-content/uploads/2015/10/Hairstyle-for-Asian-men.jpg'},
  {gender: FEMALE, src: 'http://www.asianonlinesingles.com/wp-content/uploads/2012/04/Dating-Asian-Woman-and-be-Successful.jpg'},
  {gender: FEMALE, src: 'http://blindgossip.com/wp-content/uploads/2011/08/asian-woman-1.jpg'},
];

$(document).ready(function() {
  ReactDOM.render(
    <App images={IMAGES} />,
    document.getElementById('app')
  );
});
